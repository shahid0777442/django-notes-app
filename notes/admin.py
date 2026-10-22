from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_pinned", "updated_at")
    list_filter = ("is_pinned",)
    search_fields = ("title", "content", "owner__username")
