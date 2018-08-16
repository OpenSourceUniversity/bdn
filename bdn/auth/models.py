import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models as m


class User(AbstractUser):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
