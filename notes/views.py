from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import NoteForm, RegisterForm
from .models import Note


class OwnedNoteMixin(LoginRequiredMixin):
    """Restrict every query to the logged-in user's own notes (others get a 404)."""

    model = Note

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteListView(OwnedNoteMixin, ListView):
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class NoteDetailView(OwnedNoteMixin, DetailView):
    template_name = "notes/note_detail.html"


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Note created.")
        return super().form_valid(form)


class NoteUpdateView(OwnedNoteMixin, UpdateView):
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Note saved.")
        return super().form_valid(form)


class NoteDeleteView(OwnedNoteMixin, DeleteView):
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("note-list")

    def form_valid(self, form):
        messages.success(self.request, "Note deleted.")
        return super().form_valid(form)


@login_required
@require_POST
def toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    note.is_pinned = not note.is_pinned
    note.save(update_fields=["is_pinned", "updated_at"])
    return redirect(request.POST.get("next") or "note-list")


def register(request):
    if request.user.is_authenticated:
        return redirect("note-list")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account has been created.")
        return redirect("note-list")
    return render(request, "registration/register.html", {"form": form})
