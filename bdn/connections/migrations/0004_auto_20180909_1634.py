# Generated by Django 2.0.2 on 2018-09-09 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connections', '0003_auto_20180909_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='email_address',
            new_name='email',
        ),
    ]
