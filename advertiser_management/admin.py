from django.contrib import admin
from .models import Ad, Advertiser


admin.site.register(Advertiser)
admin.site.register(Ad)
