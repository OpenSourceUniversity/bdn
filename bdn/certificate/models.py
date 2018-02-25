from django.db import models as m

# Create your models here.
class Certificate(m.Model):
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
