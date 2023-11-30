from django.shortcuts import render, get_object_or_404
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel
from django.shortcuts import redirect
from .forms import AdForm
from django.urls import reverse
from datetime import datetime
from django.views.generic import View, TemplateView
from django.db.models.functions import ExtractHour
from django.db.models import Count, F


class HomeView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        advertise = Ad.objects.annotate(advertiser_name=F('advertiser__name'))
        for ad in advertise:
            ViewModel.objects.create(ad=ad, ip=request.user.ip, view_time=datetime.now())

        context = {'advertisers': advertisers}

        return render(request, 'advertiser_management/ads.html', context)


class AdIncClicksView(View):

    @staticmethod
    def get(request, object_id, *args, **kwargs):
        ad = get_object_or_404(Ad, id=object_id)
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

        qs_clicks = (Click.objects.values('ad__title').
                     annotate(click_time=ExtractHour('click_time')).
                     annotate(click_count=Count('id')))
        qs_views = (ViewModel.objects.values('ad__title').
                    annotate(view_time=ExtractHour('view_time')).
                    annotate(view_count=Count('id')))

        total_clicks = Click.objects.count()
        total_views = ViewModel.objects.count()
        ctr = total_clicks / total_views
        # qs_ads = ((Ad.objects.values_list('id', flat=True).
        #           annotate(clicks_time=ExtractHour('click__click_time'))).
        #           annotate(views_time=ExtractHour('view__click_time')).
        #           annotate(clicks_count=Count('id')).
        #           annotate(views_count=Count('id')))

        average_view_time = ViewModel.objects.values_list('view_time', flat=True)
        average_click_time = Click.objects.values_list('click_time', flat=True)
        view_hours = map(lambda t: t.hour + (t.minute / 60.0), average_view_time)
        click_hours = map(lambda t: t.hour + (t.minute / 60.0), average_click_time)
        average = sum(click_hours) - sum(view_hours)

        # average_view_time = ViewModel.objects.aggregate(avg_view_time=Avg('view_time'))
        # average_click_time = Click.objects.aggregate(avg_click_time=Avg('click_time'))
        # average = average_click_time - average_view_time

        clicks_views = zip(qs_views, qs_clicks)
        return render(request, 'advertiser_management/report.html',
                      {
                       'ctr': ctr.__round__(2),
                       'average': average,
                       'clicks_views': clicks_views
                       })
