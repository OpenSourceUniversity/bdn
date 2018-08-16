# Generated by Django 2.0.2 on 2018-08-16 10:38

import bdn.profiles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_profile_type', models.PositiveSmallIntegerField(choices=[(bdn.profiles.models.ProfileType(1), 1), (bdn.profiles.models.ProfileType(2), 2), (bdn.profiles.models.ProfileType(3), 3)], default=bdn.profiles.models.ProfileType(1))),
                ('first_name', models.CharField(blank=True, max_length=70, null=True)),
                ('last_name', models.CharField(blank=True, max_length=70, null=True)),
                ('learner_email', models.EmailField(blank=True, max_length=70, null=True)),
                ('learner_position', models.CharField(blank=True, max_length=70, null=True)),
                ('learner_specialisation', models.CharField(blank=True, max_length=70, null=True)),
                ('learner_about', models.TextField(blank=True, max_length=500, null=True)),
                ('public_profile', models.BooleanField(default=False)),
                ('learner_site', models.CharField(blank=True, max_length=70, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=70, null=True)),
                ('learner_country', models.CharField(blank=True, max_length=70, null=True)),
                ('learner_avatar', models.CharField(blank=True, max_length=100, null=True)),
                ('academy_name', models.CharField(blank=True, max_length=70, null=True)),
                ('academy_website', models.CharField(blank=True, max_length=70, null=True)),
                ('academy_email', models.EmailField(blank=True, max_length=70, null=True)),
                ('academy_country', models.CharField(blank=True, max_length=70, null=True)),
                ('academy_about', models.TextField(blank=True, max_length=500, null=True)),
                ('academy_logo', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=70, null=True)),
                ('company_website', models.CharField(blank=True, max_length=70, null=True)),
                ('company_email', models.EmailField(blank=True, max_length=70, null=True)),
                ('company_country', models.CharField(blank=True, max_length=70, null=True)),
                ('company_about', models.TextField(blank=True, max_length=500, null=True)),
                ('company_logo', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
