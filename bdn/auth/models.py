import uuid
from enum import IntEnum
from django.contrib.auth.models import AbstractUser
from django.db import models as m


class SignUpStep(IntEnum):
    EMAIL = 1
    PASSPHRASE = 2
    SEED = 3
    SEED_CHECKED = 4
    CREATED = 5


class User(AbstractUser):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class SignUp(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = m.EmailField(max_length=70, blank=True, null=True)
    step = m.PositiveSmallIntegerField(
        default=SignUpStep.EMAIL,
        choices=[(_.value, _.name) for _ in SignUpStep])
    modified = m.DateTimeField(auto_now=True)
    email_sent = m.BooleanField(default=False)

    def __str__(self):
        return self.email
