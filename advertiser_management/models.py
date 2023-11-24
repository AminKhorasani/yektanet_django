from django.db import models

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    link = models.CharField(max_length=400)
    img_url = models.CharField(max_length=400)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

