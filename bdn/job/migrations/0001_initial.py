# Generated by Django 2.0.2 on 2018-08-16 10:38

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skill', '0001_initial'),
        ('company', '0001_initial'),
        ('industry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=130)),
                ('location', models.CharField(max_length=130)),
                ('salary', models.CharField(blank=True, max_length=130, null=True)),
                ('overview', models.TextField(max_length=500)),
                ('description', models.TextField()),
                ('external_link', models.URLField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('posted', models.DateField(auto_now_add=True)),
                ('closes', models.DateField(blank=True, null=True)),
                ('experience', models.CharField(max_length=130)),
                ('hours', models.CharField(max_length=130)),
                ('job_type', models.CharField(max_length=130, null=True)),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=70), default=[], size=None)),
                ('is_featured', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Company')),
                ('industries', models.ManyToManyField(to='industry.Industry')),
                ('skills', models.ManyToManyField(to='skill.Skill')),
            ],
        ),
    ]
