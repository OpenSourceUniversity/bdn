# Generated by Django 2.0.2 on 2018-09-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_remove_transaction_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='value',
            field=models.FloatField(),
        ),
    ]