from enum import IntEnum
from django.conf import settings
from django.db import models as m
from django.db.models.signals import post_save
from django.dispatch import receiver


def avatar_upload_path(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.id, filename)


class ProfileType(IntEnum):
    LEARNER = 1
    ACADEMY = 2
    BUSINESS = 3


class Profile(m.Model):
    active_profile_type = m.PositiveSmallIntegerField(
        default=ProfileType.LEARNER,
        choices=[(_.value, _.name) for _ in ProfileType])
    user = m.OneToOneField(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
    first_name = m.CharField(max_length=70, blank=True, null=True)
    last_name = m.CharField(max_length=70, blank=True, null=True)
    learner_email = m.EmailField(max_length=70, blank=True, null=True)
    learner_position = m.CharField(max_length=70, blank=True, null=True)
    learner_specialisation = m.CharField(
        max_length=70, blank=True, null=True)
    learner_about = m.TextField(max_length=500, blank=True, null=True)
    public_profile = m.BooleanField(default=False)
    learner_site = m.CharField(max_length=70, blank=True, null=True)
    phone_number = m.CharField(max_length=70, blank=True, null=True)
    learner_country = m.CharField(max_length=70, blank=True, null=True)
    learner_avatar = m.CharField(max_length=100, blank=True, null=True)
    academy_name = m.CharField(max_length=70, blank=True, null=True)
    academy_website = m.CharField(max_length=70, blank=True, null=True)
    academy_email = m.EmailField(max_length=70, blank=True, null=True)
    academy_country = m.CharField(max_length=70, blank=True, null=True)
    academy_about = m.TextField(max_length=500, blank=True, null=True)
    academy_logo = m.CharField(max_length=100, blank=True, null=True)
    company_name = m.CharField(max_length=70, blank=True, null=True)
    company_website = m.CharField(max_length=70, blank=True, null=True)
    company_email = m.EmailField(max_length=70, blank=True, null=True)
    company_country = m.CharField(max_length=70, blank=True, null=True)
    company_about = m.TextField(max_length=500, blank=True, null=True)
    company_logo = m.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
