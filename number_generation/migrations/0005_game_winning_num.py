# Generated by Django 3.0.7 on 2020-07-02 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('number_generation', '0004_guess'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winning_num',
            field=models.IntegerField(default=0),
        ),
    ]