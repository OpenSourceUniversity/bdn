# Generated by Django 2.0.2 on 2018-09-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0005_auto_20180921_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='connection',
            name='email_sent_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
