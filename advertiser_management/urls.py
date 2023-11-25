from django.urls import path

from advertiser_management import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='advertiser_list'),
    path('click/<int:object_id>/', views.AdIncClicksView.as_view(), name='detail'),
    path('ad_create/', views.AdCreatorView.as_view(), name='ad_create'),
]