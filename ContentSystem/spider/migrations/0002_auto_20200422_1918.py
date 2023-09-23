# Generated by Django 3.0.5 on 2020-04-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='Spiders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_id', models.IntegerField(max_length=11)),
                ('url_type', models.SmallIntegerField(max_length=3)),
                ('start_urls', models.TextField()),
                ('allowed_domains', models.CharField(max_length=255)),
                ('list_xpath', models.CharField(max_length=255)),
                ('url_contain', models.CharField(max_length=100)),
                ('url_no_contain', models.CharField(max_length=100)),
                ('rules', models.TextField()),
                ('spider_name', models.CharField(max_length=100)),
            ],
        ),
    ]
