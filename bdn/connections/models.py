import uuid
from django.db import models as m
from django.conf import settings as s


class Connection(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(
        s.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True,
        related_name='self_connections')
    user = m.ForeignKey(s.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True)
    first_name = m.CharField(max_length=70)
    last_name = m.CharField(max_length=70)
    email_address = m.CharField(max_length=130, blank=True, null=True)
    company_name = m.CharField(max_length=130, blank=True, null=True)
    position_title = m.CharField(max_length=130, blank=True, null=True)
    connected_on = m.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class FileUpload(m.Model):
    created = m.DateTimeField(auto_now_add=True)
    owner = m.ForeignKey(
        s.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True)
    datafile = m.FileField()

    def __str__(self):
        return self.owner.username
