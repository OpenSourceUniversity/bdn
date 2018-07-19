from django.db import models as m
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Certificate(m.Model):
    user_eth_address = m.CharField(max_length=70, default='None')
    uid = m.PositiveIntegerField(unique=True)
    index = m.PositiveIntegerField(unique=True)
    academy = m.CharField(max_length=42)
    course = m.CharField(max_length=42)
    learner = m.CharField(max_length=42)
    name = m.CharField(max_length=70)
    subject = m.CharField(max_length=70)
    verified = m.BooleanField(default=False)
    score = m.PositiveSmallIntegerField(default=0)
    creator = m.CharField(max_length=42)
    expiration_date = m.DateTimeField()

    def __str__(self):
        return self.name
