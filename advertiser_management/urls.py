from django.urls import path, include

from advertiser_management import views

urlpatterns = [
    path('', views.HomeViewAPI.as_view(), name='advertiser_list'),
    path('click/<int:object_id>/', views.AdIncClicksView.as_view(), name='detail'),
    path('ad_creator/', views.AdCreatorViewAPI.as_view(), name='ad_creator'),
    path('advertiser_creator/', views.AdvertiserCreatorAPI.as_view(), name='advertiser_creator'),
    path('report/', views.ReportView.as_view(), name='view_reports'),
    path('api_report/', views.ReportAPI.as_view(), name='api_report'),
]
