# Generated by Django 4.1.2 on 2022-11-10 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pojistenci', '0016_alter_seznampojisteni_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seznampojisteni',
            name='poznamka',
            field=models.TextField(blank=True, null=True, verbose_name='Poznámka'),
        ),
    ]