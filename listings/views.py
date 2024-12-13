from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorator import is_landlord
from .models import *
from django.core.paginator import Paginator
from django.core.mail import send_mail


def listings(request):
    user = request.user
    
    queryset = Listing.objects.filter(units_available__gt=0).order_by("-views")
    listings_per_page = 6
    paginator = Paginator(queryset, listings_per_page)
    page_number = request.GET.get("page")
    listings_page = paginator.get_page(page_number)
    context = {
        "listings_page": listings_page,
        "listings":listings,
        "user":user
        }
    return render(request, "listings/listings.html", context)


# Create your views here.
@is_landlord
@login_required(login_url="login")
def addListings(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.landlord = request.user
            form.save()  # Save the form with the updated listing
            messages.success(request, "Property added successfully", extra_tags="success")
            return redirect("landlord-dashboard")

    form = ListingForm(initial={"landlord": request.user})
    return render(request, "listings/AddProperty.html", {"form": form})

def listingDetails(request, id):
    listing = get_object_or_404(Listing, id=id)
    listing.views += 1
    listing.save()
    context = {"listing": listing}

    return render(request, "listings/propertyDetails.html", context)


def editListing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == "POST":
        form = EditListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(
                request, listing.title + " Updated successfully", extra_tags="success"
            )
            return redirect("landlord-dashboard")
    else:
        form = EditListingForm(instance=listing)
    context = {"listing": listing, "form": form}
    return render(request, "listings/editProperty.html", context)


def deleteListing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == "POST":
        listing.delete()
        return redirect("landlord-dashboard")
    return render(request, "listings/deleteProperty.html", {"listing": listing})


def search_listings(request):
    form = ListingSearchForm(request.GET)
    listings = Listing.objects.all()

    if form.is_valid():
        status = form.cleaned_data.get("status")
        bedrooms = form.cleaned_data.get("bedrooms")
        bathrooms = form.cleaned_data.get("bathrooms")
        location = form.cleaned_data.get("location")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")

        if bedrooms:
            listings = listings.filter(bedrooms=bedrooms)

        if bathrooms:
            listings = listings.filter(bathrooms=bathrooms)

        if status:
            listings = listings.filter(status=status)
        if location:
            listings = listings.filter(title__icontains=location)

        if min_price is not None:
            listings = listings.filter(price__gte=min_price)

        if max_price is not None:
            listings = listings.filter(price__lte=max_price)

    context = {"form": form, "listings": listings}

    return render(request, "listings/search_listing.html", context)


def buy_listings(request):
    properties = Listing.objects.filter(status='sale')

    context = {
        'properties': properties,
    }

    return render(request, 'listings/buy.html', context)

def rent_listings(request):
    properties = Listing.objects.filter(status='rent')

    context = {
        'properties': properties,
    }

    return render(request, 'listings/rent.html', context)


def request_listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == 'POST':
        form = ViewRequestForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']

            # Create a new view request object
            view_request = ViewRequest(
                user=request.user,
                listing=listing,
                message=message
            )
            view_request.save()

            # Send an email to the landlord
            subject = 'Listing View Request'
            email_message = f'A view request has been made for your listing: {listing.title}\n\nMessage: {message}'
            send_mail(subject, email_message, 'errorcode.locked@gmail.com', [listing.landlord.email])

            return redirect('home')  # Redirect to a success page
    else:
        form = ViewRequestForm()

    return render(request, 'listings/property_inquiry.html', {'form': form})