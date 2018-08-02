import uuid
from django.db import models as m
from bdn.course.models import Skill, Category
from django.contrib.postgres.fields import ArrayField


class Company(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)
    eth_address = m.CharField(max_length=42, blank=True, null=True)
    verified = m.BooleanField(default=False)

    def __str__(self):
        return self.name

class Job(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = m.CharField(max_length=130)
    location = m.CharField(max_length=130)
    salary = m.CharField(max_length=130, blank=True, null=True)
    overview = m.TextField(max_length=500)
    skills = m.ManyToManyField(Skill)
    description = m.TextField()
    external_link = m.URLField(blank=True, null=True)
    image_url = m.URLField(blank=True, null=True)
    company = m.ForeignKey(
        Company, blank=True, null=True, on_delete=m.SET_NULL)
    categories = m.ManyToManyField(Category)
    posted = m.DateField(auto_now_add=True)
    closes = m.DateField(blank=True, null=True)
    experience = m.CharField(max_length=130)
    hours = m.CharField(max_length=130)
    job_type = m.CharField(max_length=130)
    languages = ArrayField(m.CharField(max_length=70), default=[])
    is_featured = m.BooleanField(default=False)

    def __str__(self):
        return self.title