import uuid
from django.db import models as m


class Skill(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)

    def __str__(self):
        return self.name


class Provider(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)

    def __str__(self):
        return self.name


class Category(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)

    def __str__(self):
        return self.name


class Course(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = m.CharField(max_length=130)
    description = m.TextField()
    external_link = m.URLField(blank=True, null=True)
    provider = m.ForeignKey(
        Provider, blank=True, null=True, on_delete=m.SET_NULL)
    tutor = m.CharField(max_length=270, blank=True, null=True)
    categories = m.ManyToManyField(Category)
    skills = m.ManyToManyField(Skill)

    def __str__(self):
        return self.title
