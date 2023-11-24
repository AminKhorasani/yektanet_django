from django.urls import path

from advertiser_management import views

urlpatterns = [
    path('', views.index, name='index'),
    path('click/<int:object_id>/', views.detail, name='detail'),
]