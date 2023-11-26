from django.db import models

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads', null=True)
    title = models.CharField(max_length=400)
    link = models.URLField()
    img_url = models.URLField()
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=100)
    view_time = models.DateTimeField()


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=100)
    click_time = models.DateTimeField()
