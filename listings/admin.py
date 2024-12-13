from django.contrib import admin
from .models import Listing,ViewRequest

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
  list_display = ("title", "price", "landlord",)
  
admin.site.register(Listing,ListingAdmin)
admin.site.register(ViewRequest)