from django.db import models

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)


class Ad(models.Model):
    title = models.CharField(max_length=400)
    link = models.CharField
    img_url = models.CharField()
    clicks = models.PositiveIntegerField()
    views = models.PositiveIntegerField()

