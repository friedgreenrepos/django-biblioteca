# Generated by Django 2.1.2 on 2018-11-07 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181106_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilo',
            name='codfisc',
            field=models.CharField(max_length=16, verbose_name='Codice fiscale'),
        ),
    ]
