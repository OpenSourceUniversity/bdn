# Generated by Django 2.0.2 on 2018-07-27 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='industries',
            new_name='categories',
        ),
    ]