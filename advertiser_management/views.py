from django.shortcuts import render, get_object_or_404
from django.views.generic import View as ViewClass, TemplateView
from advertiser_management.models import Advertiser, Ad, Click, View
from django.shortcuts import redirect
from .forms import AdForm
from django.urls import reverse
from datetime import datetime
from django.db.models.functions import ExtractHour
from django.db.models import Count, F
from rest_framework import viewsets, generics, permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .serializers import AdSerializer, AdvertiserSerializer, ClickSerializer
from .services import *

#========== API ===========


class HomeViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = serializers.AdSerializer(Ad.objects.order_by("id").all(), many=True)
        advertise = Ad.objects.annotate(advertiser_name=F('advertiser__name'))
        for ad in advertise:
            View.objects.create(ad=ad, ip=request.ip, view_time=datetime.now())
        return Response(serializer.data)


class AdCreatorViewAPI(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        serializer = serializers.AdSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=400, data=serializer.errors)


class AdvertiserCreatorAPI(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        serializer = serializers.AdvertiserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=400, data=serializer.errors)


class ReportAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        qs_clicks = (Click.objects.values('ad__title').
                     annotate(click_time=ExtractHour('click_time')).
                     annotate(click_count=Count('id')))
        qs_views = (View.objects.values('ad__title').
                    annotate(view_time=ExtractHour('view_time')).
                    annotate(view_count=Count('id')))

        total_clicks = get_total(Click)
        total_views = get_total(View)
        ctr_total = total_clicks / total_views

        average_view_time = View.objects.values_list('view_time', flat=True)
        average_click_time = Click.objects.values_list('click_time', flat=True)
        view_hours = map(lambda t: t.hour + (t.minute / 60.0), average_view_time)
        click_hours = map(lambda t: t.hour + (t.minute / 60.0), average_click_time)
        average = sum(click_hours) - sum(view_hours)

        clicks_views = zip(qs_views, qs_clicks)

        out = []
        for view, click in clicks_views:
            out.append(
                dict(time=click['click_time'], total_clicks=click['click_count'], total_views=view['view_count'],
                     ctr=click['click_count'] / view['view_count'], advertise=click['ad__title']))

        result = {'ctr_total': ctr_total.__round__(2),
                  'average': average,
                  'ads': out
                  }

        return Response(result)

# ========= END ==============


class HomeView(TemplateView):

    @staticmethod
    def get(request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        advertise = Ad.objects.annotate(advertiser_name=F('advertiser__name'))
        for ad in advertise:
            View.objects.create(ad=ad, ip=request.ip, view_time=datetime.now())

        context = {'advertisers': advertisers}

        return render(request, 'advertiser_management/ads.html', context)


class AdIncClicksView(ViewClass):

    @staticmethod
    def get(request, object_id, *args, **kwargs):
        ad = get_object_or_404(Ad, id=object_id)
        Click.objects.create(ad=ad, ip=request.ip, click_time=datetime.now())
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
                     annotate(click_time=ExtractHour('click_time')).
                     annotate(click_count=Count('id')))
        qs_views = (View.objects.values('ad__title').
                    annotate(view_time=ExtractHour('view_time')).
                    annotate(view_count=Count('id')))

        total_clicks = get_total(Click)
        total_views = get_total(View)
        ctr = total_clicks / total_views

        average_view_time = View.objects.values_list('view_time', flat=True)
        average_click_time = Click.objects.values_list('click_time', flat=True)
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
