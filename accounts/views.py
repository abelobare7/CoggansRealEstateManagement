from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from listings.models import Listing
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from tenantMngt.models import Tenant

def index(request):
    listings = Listing.objects.order_by('-views')

    types = Listing._meta.get_field('property_type').choices
    context = {
        "listings": listings,
        "types":types
        }
    return render(request, "index.html", context)


def registerUser(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "account created successfully, login in here",
                extra_tags="success",
            )
            return redirect("login")

    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "accounts/registerUser.html", context)


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == "landlord":
                    return redirect("landlord-dashboard")
                else:
                    return redirect("home")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/loginUser.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")

def viewTenants(request):
    tenants = Tenant.objects.all()
    context = {"tenants":tenants}
    return render(request, 'accounts/index.html', context)
