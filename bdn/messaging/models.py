import uuid
from django.db import models as m
from django.conf import settings


class Thread(m.Model):
    class Meta:
        ordering = ['-modified']

    id = m.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Thread owner",
        related_name="self_threads",
        on_delete=m.CASCADE)
    opponent = m.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Thread opponent",
        on_delete=m.CASCADE)
    modified = m.DateTimeField(auto_now=True)

    def __str__(self):
        return "Chat with {0}".format(self.opponent.username)


class Message(m.Model):
    class Meta:
        ordering = ['-created']

    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = m.ForeignKey(Thread, related_name="messages", on_delete=m.CASCADE)
    sender = m.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Author",
        related_name="messages", on_delete=m.CASCADE)
    text = m.TextField(verbose_name="Message text")
    read = m.BooleanField(verbose_name="Read", default=False)
    created = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
