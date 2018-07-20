from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def avatar_upload_path(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=70, blank=True, null=True)
    last_name = models.CharField(max_length=70, blank=True, null=True)
    learner_email = models.EmailField(max_length=70, blank=True, null=True)
    learner_position = models.CharField(max_length=70, blank=True, null=True)
    learner_specialisation = models.CharField(max_length=70, blank=True, null=True)
    learner_about = models.TextField(max_length=500, blank=True, null=True)
    learner_site = models.CharField(max_length=70, blank=True, null=True)
    phone_number = models.CharField(max_length=70, blank=True, null=True)
    learner_country = models.CharField(max_length=70, blank=True, null=True)
    #learner_avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    academy_name = models.CharField(max_length=70, blank=True, null=True)
    academy_website = models.CharField(max_length=70, blank=True, null=True)
    academy_email = models.EmailField(max_length=70, blank=True, null=True)
    academy_country = models.CharField(max_length=70, blank=True, null=True)
    academy_about = models.TextField(max_length=500, blank=True, null=True)
    #academy_logo = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    company_name = models.CharField(max_length=70, blank=True, null=True)
    company_website = models.CharField(max_length=70, blank=True, null=True)
    company_email = models.EmailField(max_length=70, blank=True, null=True)
    company_country = models.CharField(max_length=70, blank=True, null=True)
    company_about = models.TextField(max_length=500, blank=True, null=True)
    #company_logo = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
