# Generated by Django 4.2.7 on 2023-11-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0007_remove_ad_clicks_remove_ad_views_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='ip',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='view',
            name='ip',
            field=models.CharField(max_length=100),
        ),
    ]