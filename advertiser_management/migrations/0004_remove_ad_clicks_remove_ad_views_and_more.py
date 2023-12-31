# Generated by Django 4.2.7 on 2023-11-25 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0003_remove_ad_ads_ad_advertiser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='views',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='views',
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_time', models.DateTimeField()),
                ('ip', models.CharField(max_length=100)),
                ('ad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='advertiser_management.ad')),
            ],
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_time', models.DateTimeField()),
                ('ip', models.CharField(max_length=100)),
                ('ad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='advertiser_management.ad')),
            ],
        ),
    ]
