# Generated by Django 2.0.2 on 2018-10-15 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0007_auto_20181008_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='owner',
        ),
        migrations.DeleteModel(
            name='FileUpload',
        ),
    ]
