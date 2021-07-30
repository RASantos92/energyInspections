from django.urls import path
from . import views
from django.contrib import admin
from inApp.models import Client as U
# class UAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(U, UAdmin)



urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index),
    path('createClient', views.createClient),
    path('loginClient', views.loginClient),
    path('clientPage', views.clientPage),
    path('destroySession', views.destroySession),
    path('aboutWhy', views.aboutWhy),
    path('services', views.services),
    path('workRequestForm', views.workRequestForm),
    path('workRequestProcess', views.workRequestProcess),
    path('adminPage', views.adminPage),
    path('adminShow/<int:clientId>', views.adminShow),
    path('reviewed/<int:requestId>', views.reviewed),
    path('adminLoginProcess', views.adminLogin),
    path('adminRegisterProcess', views.adminRegister),
    path('adminLoginPage1234561231548462858', views.adminLoginPage),
    path('adminEdit', views.adminEdit),
    path('adminEditProcess', views.adminEditProcess),
    path('showWorkR/<int:wRId>', views.inspectionRequestView),
    path('deleteWorkR/<int:wRId>', views.deleteWorkR),
    path('clientEdit/<int:clientId>', views.clientEdit),
    path('clientEditProcess', views.clientEditProcess),
    path('blogs', views.root)
]
#  life.energy@att.net
#  Sunnie69