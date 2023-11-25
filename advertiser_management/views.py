from django.shortcuts import render
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel
from django.shortcuts import redirect, get_object_or_404
from .forms import AdForm
from django.urls import reverse
from datetime import datetime
from django.views.generic import View, TemplateView, RedirectView


class HomeView(TemplateView):
    template_name = 'advertiser_management/ads.html'

    def get_context_data(self, **kwargs):
        advertisers = Advertiser.objects.all()

        for advertiser in advertisers:
            for ad in advertiser.ads.all():
                ViewModel.objects.create(ad=ad, ip='', view_time=datetime.now())
        context = {'advertisers': advertisers}
        return context


class AdIncClicksView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'ad-detail'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, id=kwargs['object_id'])
        return ad.link


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
