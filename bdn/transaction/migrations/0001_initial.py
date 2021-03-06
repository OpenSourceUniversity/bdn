# Generated by Django 2.0.2 on 2018-09-20 12:57

import bdn.transaction.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_type', models.PositiveSmallIntegerField(choices=[(1, 'DEPOSIT'), (2, 'WITHDRAW')], default=bdn.transaction.models.TransactionType(2))),
                ('currency', models.CharField(default='EDU', max_length=3)),
                ('value', models.PositiveSmallIntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('sender', models.CharField(max_length=42)),
                ('receiver', models.CharField(max_length=42)),
                ('tx_hash', models.CharField(blank=True, max_length=70, null=True)),
                ('holder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_holder', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
