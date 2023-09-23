# Generated by Django 3.0.5 on 2020-04-22 11:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0004_auto_20200422_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='spider',
            name='add_time',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spider',
            name='update_time',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='spider',
            name='cate_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='spider',
            name='url_type',
            field=models.PositiveSmallIntegerField(),
        ),
    ]