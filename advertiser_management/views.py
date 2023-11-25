from django.shortcuts import render
from advertiser_management.models import Advertiser, Ad, Click, View
from django.shortcuts import redirect
from .forms import AdForm
from django.urls import reverse
from datetime import datetime


def index(request):
    advertisers = Advertiser.objects.all()
    context = {'advertisers': advertisers}

    for advertiser in advertisers:
        ads_list = advertiser.ads.all()
        for ad in ads_list:
            View.objects.create(ad=ad, ip='', view_time=datetime.now())

    return render(request, 'advertiser_management/ads.html', context)


def ad_inc_clicks(request, object_id):
    ad = Ad.objects.get(id=object_id)
    Click.objects.create(ad=ad, ip='', click_time=datetime.now())
    return redirect(ad.link)


def ad_creator(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        form.save()
    if request.method == 'GET':
        context = {'form': form}
        return render(request,'advertiser_management/ad_create.html', context)
    else:
        return redirect(reverse('advertiser_list'))
