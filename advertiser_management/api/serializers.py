from rest_framework import serializers
from advertiser_management.services import *


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = ['name', 'ads']

    @staticmethod
    def get_ads(instance):
        ads_queryset = Ad.objects.filter(advertiser=instance)
        serializer = AdSerializer(read_only=True, instance=ads_queryset, many=True)
        return serializer.data


class AdSerializer(serializers.Serializer):
    approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ad
        fields = ['advertiser', 'title', 'image', 'link', 'approved', 'ctr']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['views_report'] = ad_views_per_hour(instance)
        data['clicks_report'] = ad_clicks_per_hour(instance)
        return data


class ClickSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    ip = serializers.IPAddressField()
    click_time = serializers.DateTimeField()
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    def create(self, validated_data):
        return Click.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ip = validated_data.get('ip', instance.ip)
        instance.click_time = validated_data.get('click_time', instance.click_time)
        instance.save()
        return instance


class ViewSerializer(serializers.Serializer):
    view_time = serializers.DateTimeField()
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    ip = serializers.IPAddressField()

    def create(self, validated_data):
        return View.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.view_time = validated_data.get('view_time', instance.view_time)
        instance.ad = validated_data.get('Ad', instance.ad)
        instance.save()
        return instance
