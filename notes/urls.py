from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.NoteListView.as_view(), name="note-list"),
    path("notes/new/", views.NoteCreateView.as_view(), name="note-create"),
    path("notes/<int:pk>/", views.NoteDetailView.as_view(), name="note-detail"),
    path("notes/<int:pk>/edit/", views.NoteUpdateView.as_view(), name="note-update"),
    path("notes/<int:pk>/delete/", views.NoteDeleteView.as_view(), name="note-delete"),
    path("notes/<int:pk>/pin/", views.toggle_pin, name="note-pin"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", views.register, name="register"),
]
