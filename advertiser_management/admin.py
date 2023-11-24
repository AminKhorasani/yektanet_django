from django.contrib import admin
from .models import Ad, Advertiser


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    readonly_fields = ['clicks', 'views']


class AdTabular(admin.TabularInline):
    model = Ad
    readonly_fields = ['views', 'clicks']


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    readonly_fields = ['clicks', 'views']
    inlines = [AdTabular]

