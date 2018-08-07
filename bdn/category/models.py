import uuid
from django.db import models as m


class Category(m.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=70)

    def __str__(self):
        return self.name
