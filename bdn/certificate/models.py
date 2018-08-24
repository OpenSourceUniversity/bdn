import uuid
from django.db import models as m
from django.conf import settings
from bdn.provider.models import Provider
from bdn.skill.models import Skill
from bdn.industry.models import Industry


class Certificate(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holder = m.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True)
    user_eth_address = m.CharField(max_length=42, default='None')
    academy_title = m.CharField(max_length=70)
    provider = m.ForeignKey(
        Provider, blank=True, null=True, on_delete=m.SET_NULL)
    academy_link = m.URLField()
    program_title = m.CharField(max_length=70, blank=True, null=True)
    course_title = m.CharField(max_length=70)
    course_link = m.URLField(blank=True, null=True)
    industries = m.ManyToManyField(Industry)
    skills = m.ManyToManyField(Skill)
    learner_eth_address = m.CharField(max_length=42)
    verified = m.BooleanField(default=False)
    verification_tx = m.CharField(max_length=100, blank=True, null=True)
    ipfs_hash = m.CharField(max_length=100, default='None')
    score = m.FloatField(default=0.0, blank=True, null=True)
    duration = m.PositiveSmallIntegerField(blank=True, null=True)
    expiration_date = m.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.course_title
