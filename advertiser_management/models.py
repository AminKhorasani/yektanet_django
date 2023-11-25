from django.db import models

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads',null=True)
    title = models.CharField(max_length=400)
    link = models.CharField(max_length=400)
    img_url = models.CharField(max_length=400)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField()
    click_time = models.DateTimeField()


class Clicks(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField()
    view_time = models.DateTimeField()
