from django.urls import path
from django.urls import include, re_path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('guide/', views.GuideView.as_view(), name='guide')
]