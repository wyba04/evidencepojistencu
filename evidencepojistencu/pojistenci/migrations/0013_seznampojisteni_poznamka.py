# Generated by Django 4.1.2 on 2022-11-08 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pojistenci', '0012_pojistenec_stat'),
    ]

    operations = [
        migrations.AddField(
            model_name='seznampojisteni',
            name='poznamka',
            field=models.TextField(null=True),
        ),
    ]
