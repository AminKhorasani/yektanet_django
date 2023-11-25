from django.contrib import admin
from .models import Ad, Advertiser


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    pass


class AdTabular(admin.TabularInline):
    model = Ad


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    inlines = [AdTabular]

