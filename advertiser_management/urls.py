from django.urls import path

from advertiser_management import views

urlpatterns = [
    path('', views.HomeViewAPI.as_view(), name='advertiser_list'),
    path('click/<int:object_id>/', views.AdIncClicksAPI.as_view(), name='detail'),
    path('ad_creator/', views.AdCreatorViewAPI.as_view(), name='ad_create'),
    path('advertiser_creator/', views.AdvertiserCreatorAPI.as_view(), name='ad_create'),
    path('view_report', views.ReportViewAPI.as_view(), name='view_report'),
    path('click_report', views.ReportClickAPI.as_view(), name='click_report')
]
