# Generated by Django 4.1.2 on 2022-11-15 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pojistenci', '0018_alter_uzivatel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PojistneUdalosti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_udalosti', models.CharField(max_length=10, null=True, verbose_name='Datum události')),
                ('cas_udalosti', models.CharField(max_length=10, null=True, verbose_name='Čas události')),
                ('popis_skody', models.TextField(null=True, verbose_name='Popis škodní údálosti')),
                ('vycisleni_skody', models.CharField(max_length=10, null=True, verbose_name='Vyčíslení hodnoty škody')),
                ('pojisteni', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pojistenci.seznampojisteni', verbose_name='Pojištění')),
            ],
            options={
                'verbose_name': 'Pojistná událost',
                'verbose_name_plural': 'Pojistné události',
            },
        ),
    ]