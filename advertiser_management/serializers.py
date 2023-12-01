from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError


class AdvertiserSerializer(serializers.Serializer):
    class Meta:
        model = Advertiser
        fields = '__all__'


class AdSerializer(serializers.Serializer):
    advertiser = serializers.PrimaryKeyRelatedField(queryset=Advertiser.objects.all())
    title = serializers.CharField()
    img_url = serializers.URLField()
    link = serializers.URLField()

    def create(self, validated_data):
        return Ad.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.advertiser = validated_data.get('advertiser', instance.advertiser)
        instance.title = validated_data.get('title', instance.title)
        instance.imgUrl = validated_data.get('img_url', instance.imgUrl)
        instance.link = validated_data.get('link', instance.link)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.save()
        return instance


class ClickSerializer(serializers.Serializer):
    class Meta:
        model = Click
        fields = '__all__'


class ViewSerializer(serializers.Serializer):
    class Meta:
        model = View
        fields = '__all__'
