# Generated by Django 4.1.2 on 2022-11-10 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pojistenci', '0014_seznampojisteni_date_created_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seznampojisteni',
            options={},
        ),
        migrations.AlterModelOptions(
            name='typpojisteni',
            options={'verbose_name': 'Druh pojištění', 'verbose_name_plural': 'Druhy pojištění'},
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='hodnota_pojisteni',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='plati_do',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='plati_od',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='pojistenec',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='poznamka',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='predmet_pojisteni',
        ),
        migrations.RemoveField(
            model_name='seznampojisteni',
            name='typ_pojisteni',
        ),
    ]
