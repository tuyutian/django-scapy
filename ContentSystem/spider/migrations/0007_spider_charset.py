# Generated by Django 3.0.5 on 2020-04-22 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0006_auto_20200422_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='spider',
            name='charset',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
