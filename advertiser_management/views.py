from django.shortcuts import render
from advertiser_management.models import Advertiser, Ad
from django.shortcuts import redirect


def index(request):
    advertisers = Advertiser.objects.all()
    context = {'advertisers': advertisers}

    for advertiser in advertisers:
        ads_list = advertiser.ads.all()
        for ad in ads_list:
            ad.inc_views()

    return render(request, 'advertiser_management/ads.html', context)


def ad_inc_clicks(request, object_id):
    ad = Ad.objects.get(id=object_id)
    ad.inc_clicks()
    return redirect(ad.link)
