# Generated by Django 2.0.2 on 2018-08-24 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0003_auto_20180824_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='eth_address',
        ),
    ]