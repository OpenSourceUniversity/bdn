# Generated by Django 2.0.2 on 2018-10-08 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_auto_20180907_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(max_length=4096, verbose_name='Message text'),
        ),
    ]