# Generated by Django 3.2.5 on 2021-07-13 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poke', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicepokemodel',
            name='pokemon',
            field=models.CharField(default='', max_length=100, verbose_name='Pokemon'),
        ),
    ]
