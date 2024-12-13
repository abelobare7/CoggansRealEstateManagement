from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard/', landlordDashboard, name='landlord-dashboard'),
    path('edit-profile/<int:id>/',editProfile,name="edit-profile"),
    path('view-profile/<int:id>/',viewProfile,name="view-profile"),
    path('tenants/',viewTenants,name="view-tenants"),
    path('properties/',viewProperties,name="properties"),
    path('reqs',viewReqs, name='reqs'),
    path('generate-report/', generate_report, name='generate-report'),
    path('request-report/', requestReport, name='request-report')
]
