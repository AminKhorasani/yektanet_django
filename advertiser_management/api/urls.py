from rest_framework.routers import DefaultRouter
from advertiser_management.api import views

router = DefaultRouter()
router.register('home', views.HomeViewAPI, basename='home')
router.register('report', views.ReportAPI, basename='report')

urlpatterns = router.urls
