# Generated by Django 3.0.5 on 2020-04-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0002_auto_20200422_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spiders',
            name='cate_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='spiders',
            name='url_type',
            field=models.SmallIntegerField(),
        ),
    ]
