# Generated by Django 2.1.3 on 2018-11-13 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_profilo_tot_richieste'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profilo',
            options={'permissions': (('sospendi_profilo', 'Sospensione dei prestiti per profilo'),), 'verbose_name_plural': 'Profili'},
        ),
        migrations.RemoveField(
            model_name='profilo',
            name='prestito_sospeso',
        ),
    ]
