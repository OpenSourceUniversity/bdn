# Generated by Django 2.0.2 on 2018-09-30 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_auto_20180907_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='external_link',
        ),
    ]
