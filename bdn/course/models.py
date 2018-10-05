import uuid
from django.db import models as m
from bdn.industry.models import Industry
from bdn.provider.models import Provider
from bdn.skill.models import Skill


class Course(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = m.CharField(max_length=130)
    program_title = m.CharField(
        max_length=130, blank=True, null=True, default=None)
    description = m.TextField()
    external_link = m.URLField()
    image_url = m.URLField(blank=True, null=True)
    provider = m.ForeignKey(
        Provider, blank=True, null=True, on_delete=m.SET_NULL)
    tutor = m.CharField(max_length=270, blank=True, null=True)
    industries = m.ManyToManyField(Industry)
    skills = m.ManyToManyField(Skill)
    duration = m.PositiveSmallIntegerField(blank=True, null=True)
    is_featured = m.BooleanField(default=False)

    def __str__(self):
        return self.title
