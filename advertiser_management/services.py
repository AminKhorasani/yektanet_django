from django.db import models
from django.db.models import Count, DateTimeField, F
from django.db.models.functions import Trunc
from .models import Ad, Advertiser, View, Click


def update_advertisers_views(advertisers: list[Advertiser], ip):
    for advertiser in advertisers:
        update_advertiser_views(advertiser, ip)


def update_advertiser_views(advertiser, ip):
    update_ads_views(advertiser.get_approved_ads(), ip)


def update_ads_views(ads: list[Ad], ip):
    for ad in ads:
        ad.inc_views(ip)


def click_per_hour(ad: Ad):
    result = Click.objects.filter(ad=ad).annotate(
        created_date=Trunc('created_time', 'hour', output_field=DateTimeField())).values('created_date').annotate(
        total_clicks=Count('id')).order_by('-created_date').annotate(ad_title=F('ad__title'))
    return result


def view_per_hour(ad: Ad):
    result = View.objects.filter(ad=ad).annotate(
        created_date=Trunc('created_time', 'hour', output_field=DateTimeField())).values('created_date').annotate(
        total_views=Count('id')).order_by('-created_date').annotate(ad_title=F('ad__title'))
    return result


def ad_views_per_hour(ad: Ad):
    return view_per_hour(ad)


def ad_clicks_per_hour(ad: Ad):
    return click_per_hour(ad)


def get_total(model: models):
    return model.objects.count()


def ctr_per_hour(ad):
    view_count = View.objects.filter(ad=1).annotate(
        time=Trunc('created_time', 'hour', output_field=DateTimeField())).values(
        'time').annotate(count=Count('id'))

    click_count = Click.objects.filter(ad=1).annotate(
        time=Trunc('created_time', 'hour', output_field=DateTimeField())).values(
        'time').annotate(count=Count('id'))