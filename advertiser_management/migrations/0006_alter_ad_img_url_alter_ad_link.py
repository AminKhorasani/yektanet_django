# Generated by Django 4.2.7 on 2023-11-26 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0005_remove_view_ad_ad_clicks_ad_views_advertiser_clicks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='img_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='ad',
            name='link',
            field=models.URLField(),
        ),
    ]