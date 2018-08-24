import uuid
from django.db import models as m
from django.conf import settings


class Provider(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)
    user = m.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True)
    verified = m.BooleanField(default=False)

    def __str__(self):
        return self.name
