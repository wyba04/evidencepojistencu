# Generated by Django 4.1.2 on 2022-11-08 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pojistenci', '0009_stat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pojistenec',
            name='jmeno',
            field=models.CharField(max_length=200, verbose_name='Jméno'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='mesto',
            field=models.CharField(max_length=100, verbose_name='Město'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='prijmeni',
            field=models.CharField(max_length=200, verbose_name='Příjmení'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='psc',
            field=models.CharField(max_length=9, verbose_name='PSČ'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='stat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pojistenci.stat', verbose_name='Stát'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='telefon',
            field=models.CharField(max_length=15, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='ulice_cp',
            field=models.CharField(max_length=200, verbose_name='Ulice a číslo popisné'),
        ),
    ]