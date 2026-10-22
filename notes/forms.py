from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "is_pinned"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title", "autofocus": True}),
            "content": forms.Textarea(attrs={"rows": 12, "placeholder": "Write your note…"}),
        }


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
