from . import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('stk-push', views.lipaNAMpesa),
    path('callback-url', views.callBack),
    path('c2b', views.c2b),
    path('validation', views.validation),
    path('confirmation', views.confirmation)
]
