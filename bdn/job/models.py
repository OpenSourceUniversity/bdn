import uuid
from django.db import models as m
from bdn.industry.models import Industry
from bdn.skill.models import Skill
from bdn.company.models import Company
from django.contrib.postgres.fields import ArrayField


class Job(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = m.CharField(max_length=130)
    location = m.CharField(max_length=130)
    salary = m.CharField(max_length=130, blank=True, null=True)
    overview = m.TextField(max_length=500)
    skills = m.ManyToManyField(Skill)
    description = m.TextField()
    image_url = m.URLField(blank=True, null=True)
    company = m.ForeignKey(
        Company, blank=True, null=True, on_delete=m.SET_NULL)
    industries = m.ManyToManyField(Industry)
    posted = m.DateField(auto_now_add=True)
    closes = m.DateField(blank=True, null=True)
    experience = m.CharField(max_length=130, blank=True, null=True)
    hours = m.PositiveSmallIntegerField(blank=True, null=True)
    languages = ArrayField(m.CharField(
        max_length=70, blank=True, null=True), default=[])
    is_featured = m.BooleanField(default=False)

    def __str__(self):
        return self.title
