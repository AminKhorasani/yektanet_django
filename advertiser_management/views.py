from django.shortcuts import render
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel
from django.shortcuts import redirect
from .forms import AdForm
from django.urls import reverse
from datetime import datetime
from django.views.generic import View, TemplateView


class HomeView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ads.all():
                ViewModel.objects.create(ad=ad, ip=request.user.ip, view_time=datetime.now())
        context = {'advertisers': advertisers}
        return render(request, 'advertiser_management/ads.html', context)


class AdIncClicksView(View):

    @staticmethod
    def get(request, object_id, *args, **kwargs):
        ad = Ad.objects.get(id=object_id)
        Click.objects.create(ad=ad, ip=request.user.ip, click_time=datetime.now())
        return redirect(ad.link)


class AdCreatorView(TemplateView):
    template_name = 'advertiser_management/ad_create.html'

    def get_context_data(self, **kwargs):
        form = AdForm()
        context = {'form': form}
        return context

    @staticmethod
    def post(request):
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('advertiser_list'))


class ReportView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        clicks = Click.objects.all()
        views = ViewModel.objects.all()
        ads_number = Ad.objects.all().count()
        context = []

        for i in range(1, ads_number + 1):
            ad_title = Ad.objects.get(id=i)
            for time in range(24):
                info = {
                    'Ad': ad_title,
                    'time': '%s:00:00 - %s:59:59' % (time, time),
                    'clicks_number_per_ad': clicks.filter(id=i, click_time__hour=time).count(),
                    'views_number_per_ad': views.filter(id=i, view_time__hour=time).count(),
                }
                context.append(info)
        return render(request, 'advertiser_management/report.html', {'context': context})