# Generated by Django 2.0.2 on 2018-09-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20180820_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='industries',
            field=models.ManyToManyField(to='industry.Industry'),
        ),
    ]