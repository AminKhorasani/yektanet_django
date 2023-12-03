from django.shortcuts import render, get_object_or_404
from django.views.generic import View as ViewClass, TemplateView
from django.shortcuts import redirect
from .forms import AdForm
from django.urls import reverse
from datetime import datetime
from django.db.models.functions import ExtractHour
from .services import *


class HomeView(TemplateView):

    @staticmethod
    def get(request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        advertise = Ad.objects.annotate(advertiser_name=F('advertiser__name'))
        for ad in advertise:
            View.objects.create(ad=ad, ip=request.ip, created_time=datetime.now())

        context = {'advertisers': advertisers}

        return render(request, 'advertiser_management/ads.html', context)


class AdIncClicksView(ViewClass):

    @staticmethod
    def get(request, object_id, *args, **kwargs):
        ad = get_object_or_404(Ad, id=object_id)
        Click.objects.create(ad=ad, ip=request.ip, created_time=datetime.now())
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


class ReportView(ViewClass):

    @staticmethod
    def get(request, *args, **kwargs):
        qs_clicks = (Click.objects.values('ad__title').
                     annotate(created_time=ExtractHour('created_time')).
                     annotate(click_count=Count('id')))
        qs_views = (View.objects.values('ad__title').
                    annotate(created_time=ExtractHour('created_time')).
                    annotate(view_count=Count('id')))

        total_clicks = get_total(Click)
        total_views = get_total(View)
        ctr = total_clicks / total_views

        average_view_time = View.objects.values_list('created_time', flat=True)
        average_click_time = Click.objects.values_list('created_time', flat=True)
        view_hours = map(lambda t: t.hour + (t.minute / 60.0), average_view_time)
        click_hours = map(lambda t: t.hour + (t.minute / 60.0), average_click_time)
        average = sum(click_hours) - sum(view_hours)

        clicks_views = zip(qs_views, qs_clicks)
        return render(request, 'advertiser_management/report.html',
                      {
                          'ctr': ctr.__round__(2),
                          'average': average,
                          'clicks_views': clicks_views
                      })
