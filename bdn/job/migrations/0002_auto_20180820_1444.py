# Generated by Django 2.0.2 on 2018-08-20 14:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20180820_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='industries',
            field=models.ManyToManyField(blank=True, to='industry.Industry'),
        ),
        migrations.AlterField(
            model_name='job',
            name='languages',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=70, null=True), default=[], size=None),
        ),
    ]
