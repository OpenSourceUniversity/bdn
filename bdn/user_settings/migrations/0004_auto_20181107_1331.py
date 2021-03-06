# Generated by Django 2.0.2 on 2018-11-07 13:31

from django.db import migrations
from bdn.utils.send_email_tasks import verification_email


def send_verification_emails(apps, schema_editor):
    User = apps.get_model('bdn_auth', 'User')
    users = User.objects.filter(usersettings__email_verified=False)
    for user in users:
        link = 'https://bdn.os.university/email-verification/{}/{}/'.format(
            user.usersettings.id,
            user.usersettings.email_verification_token)
        if user.email:
            verification_email.delay(
                link,
                user.email
                )


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0003_auto_20181107_1328'),
    ]

    operations = [
        migrations.RunPython(send_verification_emails)
    ]
