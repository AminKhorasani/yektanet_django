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
