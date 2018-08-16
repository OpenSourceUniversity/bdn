import uuid
from django.conf import settings
from django.db import models as m
from django_fsm import FSMField, transition
from bdn.profiles.models import ProfileType


class Verification(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = FSMField(default='open')
    tx_hash = m.CharField(max_length=70, null=True, blank=True)
    block_hash = m.CharField(max_length=70, null=True, blank=True)
    block_number = m.IntegerField(default=0)
    certificate = m.ForeignKey(
        'certificate.Certificate', on_delete=m.SET_NULL, null=True)
    granted_to = m.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True,
        related_name='received_verifications')
    verifier = m.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True,
        related_name='granted_verifications')
    verifier_type = m.PositiveSmallIntegerField(
        default=ProfileType.LEARNER,
        choices=[(_, _.value) for _ in ProfileType])
    meta_ipfs_hash = m.CharField(max_length=50, null=True, blank=True)
    date_created = m.DateTimeField(auto_now_add=True)
    date_last_modified = m.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tx_hash or ''

    @transition(field=state, source=['requested', 'pending'], target='open')
    def move_to_open(self):
        pass

    @transition(field=state, source='open', target='pending')
    def move_to_pending(self):
        pass

    @transition(field=state, source='pending', target='verified')
    def move_to_verified(self):
        pass

    @transition(field=state, source='pending', target='revoked')
    def move_to_revoked(self):
        pass
