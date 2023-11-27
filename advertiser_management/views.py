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
        total_clicks = 0
        total_views = 0
        clicks_views = []

        for j in range(1, ads_number + 1):
            ad_object = Ad.objects.get(id=j)
            ad_title = ad_object.title
            for time in range(24):
                clicks_count = clicks.filter(ad__id=j, click_time__hour=time).count()
                views_count = views.filter(ad__id=j, view_time__hour=time).count()
                total_clicks += clicks_count
                total_views += views_count
                ctr = 0
                if views_count != 0:
                    ctr = (clicks_count / views_count).__round__(2)

                clicks_views.append({
                    'time': '%s:00:00 - %s:59:59' % (time, time),
                    'ctr': ctr,
                    'clicks_number_per_ad': clicks_count,
                    'views_number_per_ad': views_count,
                    'Ad': ad_title,

                })

        sorted_clicks_views = sorted(clicks_views, key=lambda i: i['ctr'], reverse=True)

        average_view_time = ViewModel.objects.values_list('view_time', flat=True)
        average_click_time = Click.objects.values_list('click_time', flat=True)
        view_hours = map(lambda t: t.hour + (t.minute / 60.0), average_view_time)
        click_hours = map(lambda t: t.hour + (t.minute / 60.0), average_click_time)
        average = sum(click_hours) - sum(view_hours)

        # average_view_time = ViewModel.objects.aggregate(avg_view_time=Avg('view_time'))
        # average_click_time = Click.objects.aggregate(avg_click_time=Avg('click_time'))
        # average =
        return render(request, 'advertiser_management/report.html',
                      {
                       'total_clicks_views': (total_clicks / total_views).__round__(2),
                       'clicks_views': sorted_clicks_views,
                       'average': average
                       })
