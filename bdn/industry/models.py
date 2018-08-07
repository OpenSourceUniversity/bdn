import uuid
from django.db import models as m


class Industry(m.Model):
    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        ordering = ('name',)

    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)

    def __str__(self):
        return self.name
