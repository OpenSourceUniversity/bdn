# Generated by Django 2.0.2 on 2018-07-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20180717_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='public_profile',
            field=models.BooleanField(default=False),
        ),
    ]
