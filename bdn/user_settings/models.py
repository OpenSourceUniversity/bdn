import uuid
from django.conf import settings
from django.db import models as m
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserSettings(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = m.OneToOneField(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
    password = m.CharField(max_length=100, default=None, null=True, blank=True)
    subscribed = m.BooleanField(default=True)
    news_subscribed = m.BooleanField(default=True)
    save_wallet = m.BooleanField(default=True)
    wallet = m.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_setttings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
