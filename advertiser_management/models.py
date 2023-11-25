from django.db import models

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads', null=True)
    title = models.CharField(max_length=400)
    link = models.CharField(max_length=400)
    img_url = models.CharField(max_length=400)


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=100)
    view_time = models.DateTimeField()


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=100)
    click_time = models.DateTimeField()
