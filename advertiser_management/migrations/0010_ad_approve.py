# Generated by Django 4.2.7 on 2023-11-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0009_alter_ad_img_url_alter_ad_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]