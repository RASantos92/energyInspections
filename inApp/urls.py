from django.urls import path
from . import views
from django.contrib import admin


from inApp.models import Client as U
class UAdmin(admin.ModelAdmin):
    pass
admin.site.register(U, UAdmin)



urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index),
    path('createClient', views.createClient),
    path('loginClient', views.loginClient),
    path('clientPage', views.clientPage),
]
#  life.energy@att.net
#  Sunnie69