from django.urls import path
from django.urls import include, re_path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about')
]