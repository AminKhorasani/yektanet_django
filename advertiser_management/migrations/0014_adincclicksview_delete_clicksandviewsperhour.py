# Generated by Django 4.2.7 on 2023-12-02 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0013_clicksandviewsperhour_alter_click_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdIncClicksView',
            fields=[
                ('view_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advertiser_management.view')),
            ],
            bases=('advertiser_management.view',),
        ),
        migrations.DeleteModel(
            name='ClicksAndViewsPerHour',
        ),
    ]
