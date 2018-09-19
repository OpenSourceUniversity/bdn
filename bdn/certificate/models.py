import uuid
from django.db import models as m
from django.conf import settings
from bdn.skill.models import Skill
from bdn.industry.models import Industry
from bdn.profiles.models import ProfileType


class Certificate(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holder = m.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=m.SET_NULL, null=True)
    user_eth_address = m.CharField(max_length=42, default='None')
    institution_title = m.CharField(max_length=70)
    institution_link = m.URLField()
    program_title = m.CharField(max_length=70, blank=True, null=True)
    certificate_title = m.CharField(max_length=70)
    course_link = m.URLField(blank=True, null=True)
    granted_to_type = m.PositiveSmallIntegerField(
        default=ProfileType.LEARNER,
        choices=[(_.value, _.name) for _ in ProfileType])
    industries = m.ManyToManyField(Industry)
    skills = m.ManyToManyField(Skill)
    ipfs_hash = m.CharField(max_length=100, default='None')
    score = m.FloatField(default=0.0, blank=True, null=True)
    duration = m.PositiveSmallIntegerField(blank=True, null=True)
    expiration_date = m.DateTimeField(blank=True, null=True)
    checksum_hash = m.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.certificate_title
