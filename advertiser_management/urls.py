from django.urls import path, include

from advertiser_management import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='advertiser_list'),
    path('click/<int:object_id>/', views.AdIncClicksView.as_view(), name='detail'),
    path('ad_creator/', views.AdCreatorView.as_view(), name='ad_creator'),
    path('report/', views.ReportView.as_view(), name='view_reports'),
    path('api/', include('advertiser_management.api.urls')),
]
