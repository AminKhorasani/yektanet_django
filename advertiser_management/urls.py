from django.urls import path

from advertiser_management import views

urlpatterns = [
    path('', views.index, name='advertiser_list'),
    path('click/<int:object_id>/', views.ad_inc_clicks, name='detail'),
    path('ad_create/', views.ad_creator, name='ad_create')
]