from rest_framework import viewsets, permissions
from .serializers import AdvertiserSerializer, AdSerializer
from advertiser_management.models import Advertiser, Ad
from advertiser_management.services import update_advertisers_views, update_advertiser_views


class HomeViewAPI(viewsets.ModelViewSet):
    serializer_class = AdvertiserSerializer
    queryset = Advertiser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        update_advertisers_views(queryset, request.ip)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        advertiser = self.get_object()
        update_advertiser_views(advertiser, request.ip)
        return super().retrieve(request, *args, **kwargs)


class ReportAPI(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.filter()

