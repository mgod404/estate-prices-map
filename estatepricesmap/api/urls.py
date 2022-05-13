from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getgeodata/', views.geo_data, name='geo-data')
]