from celery import shared_task
from bdn.auth.models import User
from .models import UserSettings


@shared_task
def create_user_settings():
    print('Start!')
    users = User.objects.all()
    for user in users:
        user_settings, created = UserSettings.objects.get_or_create(user=user)
        if created:
            print('Created!')
            user_settings.save()
