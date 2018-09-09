# Generated by Django 2.0.2 on 2018-09-09 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connections', '0002_remove_fileupload_owner_eth_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('email_address', models.CharField(blank=True, max_length=130, null=True)),
                ('company_name', models.CharField(blank=True, max_length=130, null=True)),
                ('position_title', models.CharField(blank=True, max_length=130, null=True)),
                ('connected_on', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='self_connections', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='connections',
            name='contacts_holder',
        ),
        migrations.DeleteModel(
            name='Connections',
        ),
    ]
