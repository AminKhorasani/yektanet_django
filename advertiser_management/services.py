from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc
from .models import *


def per_hour(model, ad):
    result = model.objects.filter(ad=ad).annotate(
        created_date=Trunc('created_on', 'hour', output_field=DateTimeField())).values('created_date').annotate(
        count=Count('id')).order_by('-created_date')
    return result


def ad_views_per_hour(ad):
    return per_hour(View, ad)


def ad_clicks_per_hour(ad):
    return per_hour(Click, ad)


def get_total(model: models):
    return model.objects.count()


def ctr_per_hour(ad):
    view_count = View.objects.filter(ad=1).annotate(
        time=Trunc('created_on', 'hour', output_field=DateTimeField())).values(
        'time').annotate(count=Count('id'))

    click_count = Click.objects.filter(ad=1).annotate(
        time=Trunc('created_on', 'hour', output_field=DateTimeField())).values(
        'time').annotate(count=Count('id'))