from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Tenant)
admin.site.register(MaintenanceRequest)
admin.site.register(Lease)
admin.site.register(PropertyInquiry)
admin.site.register(Contact)