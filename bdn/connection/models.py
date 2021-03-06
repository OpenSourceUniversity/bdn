import uuid
from django.db import models as m
from django.conf import settings as s


class Connection(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(
        s.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True,
        related_name='self_connection')
    user = m.ForeignKey(s.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True)
    full_name = m.CharField(max_length=70)
    email = m.CharField(max_length=130, blank=True, null=True)
    company_name = m.CharField(max_length=130, blank=True, null=True)
    position_title = m.CharField(max_length=130, blank=True, null=True)
    connected_on = m.DateTimeField(blank=True, null=True)
    email_sent = m.BooleanField(default=False)
    email_sent_on = m.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.full_name
