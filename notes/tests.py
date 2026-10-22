from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note

User = get_user_model()


class NoteTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pass12345!")
        self.bob = User.objects.create_user("bob", password="pass12345!")
        self.note = Note.objects.create(owner=self.alice, title="Groceries", content="milk, eggs")
        self.client.login(username="alice", password="pass12345!")

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(reverse("note-list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_create_sets_owner(self):
        resp = self.client.post(reverse("note-create"), {"title": "Idea", "content": "x"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Note.objects.get(title="Idea").owner, self.alice)

    def test_cannot_access_other_users_note(self):
        other = Note.objects.create(owner=self.bob, title="Secret")
        for name in ("note-detail", "note-update", "note-delete"):
            resp = self.client.get(reverse(name, args=[other.pk]))
            self.assertEqual(resp.status_code, 404, name)
        resp = self.client.post(reverse("note-pin", args=[other.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_list_only_shows_own_notes(self):
        Note.objects.create(owner=self.bob, title="Secret")
        resp = self.client.get(reverse("note-list"))
        self.assertContains(resp, "Groceries")
        self.assertNotContains(resp, "Secret")

    def test_search(self):
        Note.objects.create(owner=self.alice, title="Work", content="meeting at 5")
        resp = self.client.get(reverse("note-list"), {"q": "meeting"})
        self.assertContains(resp, "Work")
        self.assertNotContains(resp, "Groceries")

    def test_pin_toggle_and_ordering(self):
        newer = Note.objects.create(owner=self.alice, title="Newer")
        self.client.post(reverse("note-pin", args=[self.note.pk]))
        self.note.refresh_from_db()
        self.assertTrue(self.note.is_pinned)
        self.assertEqual(list(Note.objects.filter(owner=self.alice))[0], self.note)
        self.assertNotEqual(newer, self.note)

    def test_delete(self):
        self.client.post(reverse("note-delete", args=[self.note.pk]))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_register_logs_in(self):
        self.client.logout()
        resp = self.client.post(
            reverse("register"),
            {"username": "carol", "password1": "S3cure-pass-77", "password2": "S3cure-pass-77"},
        )
        self.assertRedirects(resp, reverse("note-list"))
        self.assertTrue(User.objects.filter(username="carol").exists())
