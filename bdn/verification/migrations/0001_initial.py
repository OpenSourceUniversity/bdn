# Generated by Django 2.0.2 on 2018-08-15 14:14

import bdn.profiles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certificate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', django_fsm.FSMField(default='open', max_length=50)),
                ('tx_hash', models.CharField(max_length=70)),
                ('block_hash', models.CharField(max_length=70)),
                ('block_number', models.IntegerField(default=0)),
                ('verifier_type', models.PositiveSmallIntegerField(choices=[(bdn.profiles.models.ProfileType(1), 1), (bdn.profiles.models.ProfileType(2), 2), (bdn.profiles.models.ProfileType(3), 3)], default=bdn.profiles.models.ProfileType(1))),
                ('meta_ipfs_hash', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('certificate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='certificate.Certificate')),
                ('granted_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_verifications', to=settings.AUTH_USER_MODEL)),
                ('verifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='granted_verifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
