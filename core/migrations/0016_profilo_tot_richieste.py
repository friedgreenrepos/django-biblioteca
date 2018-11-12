# Generated by Django 2.1.3 on 2018-11-12 22:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20181112_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilo',
            name='tot_richieste',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(4)]),
        ),
    ]
