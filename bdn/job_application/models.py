import uuid
from django.db import models as m
from django_fsm import FSMField, transition
from bdn.job.models import Job
from django.conf import settings


class JobApplication(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = m.ForeignKey(Job, blank=True, null=True, on_delete=m.SET_NULL)
    issuer = m.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=m.SET_NULL,
        related_name='application_issuer')
    state = FSMField(default='open')
    date_created = m.DateTimeField(auto_now_add=True)
    date_last_modified = m.DateTimeField(auto_now=True)

    def __str__(self):
        return self.issuer

    @transition(field=state, source=['requested'], target='approved')
    def move_to_approved(self):
        pass

    @transition(field=state, source=['requested'], target='rejected')
    def move_to_rejected(self):
        pass
