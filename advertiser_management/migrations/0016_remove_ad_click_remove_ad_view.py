# Generated by Django 4.2.7 on 2023-12-02 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0015_ad_click_ad_view_alter_click_ad_alter_view_ad_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='click',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='view',
        ),
    ]