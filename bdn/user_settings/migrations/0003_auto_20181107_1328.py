# Generated by Django 2.0.2 on 2018-11-07 13:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0002_auto_20181030_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='email_verification_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
