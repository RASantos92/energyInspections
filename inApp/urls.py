from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('createClient', views.createClient),
    path('loginClient', views.loginClient),
    path('clientPage', views.clientPage),
]
