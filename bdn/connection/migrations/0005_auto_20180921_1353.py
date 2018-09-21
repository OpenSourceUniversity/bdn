# Generated by Django 2.0.2 on 2018-09-21 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0004_auto_20180909_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='self_connection', to=settings.AUTH_USER_MODEL),
        ),
    ]
