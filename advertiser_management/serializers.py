from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'
        read_only_fields = ['id']


class AdSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    img_url = serializers.CharField()
    link = serializers.CharField()
    advertiser = serializers.PrimaryKeyRelatedField(queryset=Advertiser.objects.all())
    approve = serializers.BooleanField()
    views = serializers.IntegerField(read_only=True)
    clicks = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return Ad.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.advertiser = validated_data.get('advertiser', instance.advertiser)
        instance.title = validated_data.get('title', instance.title)
        instance.img_url = validated_data.get('img_url', instance.img_url)
        instance.link = validated_data.get('link', instance.link)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.save()
        return instance


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


# class AdvertiserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Advertiser
#         fields = '__all__'
#
#
# class AdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ad
#         fields = '__all__'
#
#
# class ClickSerializer(serializers.ModelSerializer):
#     click_hour = serializers.CharField()
#
#     class Meta:
#         model = Click
#         fields = '__all__'
#
#
# class ViewSerializer(serializers.ModelSerializer):
#     ctr = serializers.CharField()
#
#     class Meta:
#         model = View
#         fields = '__all__'
#
