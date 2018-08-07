import uuid
from django.db import models as m


class Company(m.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)
    eth_address = m.CharField(max_length=42, blank=True, null=True)
    verified = m.BooleanField(default=False)

    def __str__(self):
        return self.name
