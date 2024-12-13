from django.urls import path
from .views import *

urlpatterns = [
    path('',listings, name='listings'),
    path('<int:listing_id>/requests',request_listing_view,name='request'),
    path('search/', search_listings, name='search_listings'),
    path('sale/', buy_listings, name='buy_listings'),
    path('rent/', rent_listings, name='rent_listings'),
    path('add-listing', addListings, name='add-listing'),
    path('<int:id>/', listingDetails, name='listing-details'),
    path('edit/<int:id>/', editListing, name='edit-listing'),
    path('delete/<int:id>/', deleteListing, name='delete-listing'),
]