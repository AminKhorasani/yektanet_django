from django.db import models
from django.urls import reverse


class Advertiser(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_approved_ads(self):
        return self.ads.filter(approve=True)

    def get_total_clicks(self):
        ads = self.ads.all()
        clicks_count = sum(ad.total_clicks() for ad in ads)
        return clicks_count

    def get_total_views(self):
        ads = self.ads.all()
        views_count = sum(ad.total_views() for ad in ads)
        return views_count

    get_total_views.short_description = 'Total views'
    get_total_clicks.short_description = 'Total  clicks'


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=400)
    link = models.URLField()
    img_url = models.URLField()
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def inc_clicks(self, ip_addr):
        Click.objects.create(ad=self, ip=ip_addr)

    def inc_views(self, ip_addr):
        View.objects.create(ad=self, ip=ip_addr)

    def total_clicks(self):
        return self.ad_click.count()

    def total_views(self):
        return self.ad_view.count()

    def get_absolute_url(self):
        return reverse('detail1', kwargs={'object_id': self.pk})

    @property
    def ctr(self):
        if self.total_views() != 0:
            return round(self.total_clicks() / self.total_views(), 2)
        return 0


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE ,related_name='ad_view')
    ip = models.GenericIPAddressField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_click')
    ip = models.GenericIPAddressField()
    created_time = models.DateTimeField(auto_now_add=True)

