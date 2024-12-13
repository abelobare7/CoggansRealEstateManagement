from django.urls import path, include
from .views import *
urlpatterns = [
    path('contact/', contact, name="contact"),
]