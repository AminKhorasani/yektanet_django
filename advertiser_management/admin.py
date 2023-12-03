from django.contrib import admin
from .models import *


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_filter = ('approve',)
    search_fields = ('title',)


class AdTabular(admin.TabularInline):
    model = Ad


@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    inlines = [AdTabular]


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    model = Click
    list_display = ['created_time']


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    model = View
    list_display = ['created_time']
