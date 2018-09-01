# Generated by Django 2.0.2 on 2018-08-29 08:29

import bdn.auth.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bdn_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('step', models.PositiveSmallIntegerField(choices=[(1, 'EMAIL'), (2, 'PASSPHRASE'), (3, 'SEED'), (4, 'SEED_CHECKED'), (5, 'CREATED')], default=bdn.auth.models.SignUpStep(1))),
            ],
        ),
    ]