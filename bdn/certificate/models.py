import uuid
from django.db import models as m
from django.contrib.postgres.fields import ArrayField
from bdn.course.models import Provider, Skill, Category


class Certificate(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_eth_address = m.CharField(max_length=42, default='None')
    academy_title = m.CharField(max_length=70)
    academy_address = m.CharField(max_length=42, blank=True, null=True)
    provider = m.ForeignKey(
        Provider, blank=True, null=True, on_delete=m.SET_NULL)
    academy_link = m.URLField()
    program_title = m.CharField(max_length=70, blank=True, null=True)
    course_title = m.CharField(max_length=70)
    course_link = m.URLField(blank=True, null=True)
    categories = m.ManyToManyField(Category)
    skills = m.ManyToManyField(Skill)
    learner_eth_address = m.CharField(max_length=42)
    verified = m.BooleanField(default=False)
    verification_tx= m.CharField(max_length=100, blank=True, null=True)
    ipfs_hash = m.CharField(max_length=100, default='None')
    score = m.FloatField(default=0.0)
    duration = m.DurationField(blank=True, null=True)
    expiration_date = m.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.course_title
