from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from listings.models import *
from listings.decorator import is_landlord
from tenantMngt.models import *
from accounts.models import CustomUser
from .forms import *
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .credentials import *
from django.http import HttpResponse, HttpResponseBadRequest,JsonResponse
import json

# Create your views here.


@login_required(login_url="login")
@is_landlord
def landlordDashboard(request):
    user = request.user
    if user.user_type == "landlord":
        listings = Listing.objects.filter(landlord=user)
        total_listings = Listing.objects.filter(landlord=user).count()
        total_views = ViewRequest.objects.filter(listing__landlord=user).count()
        inqs = ViewRequest.objects.filter(listing__in=listings)
        tenants = Tenant.objects.filter(listing__in=listings)
    context = {
        "listings": listings,
        "inqs" : inqs,"tenants": tenants,
        'total_listings': total_listings,
        'total_views': total_views
        }
    return render(request, "landlordManager/dashboardNav.html", context)

def editProfile(request, id):
    profile = get_object_or_404(CustomUser, id=id)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Profile Updated successfully",
                extra_tags="success",
            )
            return redirect("landlord-dashboard")
    else:
        form = EditProfileForm(instance=profile)
    context = {"profile": profile, "form": form}
    return render(request, "landlordManager/editProfile.html", context)

def viewProfile(request, id):
    user = get_object_or_404(CustomUser, id=id)
    context = {"user": user}

    return render(request, "landlordManager/viewProfile.html", context)
    
def viewTenants(request):
    user = request.user
    if user.user_type == "landlord":
        listings = Listing.objects.filter(landlord=user)
        tenants = Tenant.objects.filter(listing__in=listings)
    context = {
        "listings":listings,
        "tenants": tenants,}
    return render(request, "landlordManager/tenants.html", context)

@login_required(login_url="login")
@is_landlord
def viewProperties(request):
    user = request.user
    if user.user_type == "landlord":
        listings = Listing.objects.filter(landlord=user)
        
    context = {"listings": listings}
    return render(request, "landlordManager/properties.html", context)
@is_landlord
def viewReqs(request):
    user = request.user
    if user.user_type == "landlord":
        reqs = ViewRequest.objects.filter(listing__landlord=user)

    context = {
        "reqs" : reqs
        }
    return render(request, "landlordManager/viewReqs.html", context)

@is_landlord
def generate_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listing_report.pdf"'
    landlord = request.user
    # Create a canvas object
    p = canvas.Canvas(response)

    # Query data from the Listing model
    listings = Listing.objects.all()

    # Set initial y position
    y = 800

    # Write the data to the PDF
    p.drawString(100, y, f"Reports for: {landlord.first_name} {landlord.last_name}")
    y -= 20
    for listing in listings:
        
        p.drawString(100, y, f"Title: {listing.title}")
        y -= 20
        p.drawString(100, y, f"Price: {listing.price}")
        y -= 20
        p.drawString(100, y, f"Property Type: {listing.get_property_type_display()}")
        y -= 20
        p.drawString(100, y, f"Status: {listing.get_status_display()}")
        y -= 20
        p.drawString(100, y, f"Units Available: {listing.units_available}")
        y -= 20
        p.drawString(100, y, f"Bedrooms: {listing.bedrooms}")
        y -= 20
        p.drawString(100, y, f"Bathrooms: {listing.bathrooms}")
        y -= 20
        p.drawString(100, y, f"Square Feet: {listing.square_feet}")
        y -= 20
        p.drawString(100, y, f"Address: {listing.address}")
        y -= 20
        p.drawString(100, y, f"City: {listing.city}")
        y -= 20
        p.drawString(100, y, f"State: {listing.state}")
        y -= 20
        p.drawString(100, y, f"Zipcode: {listing.zipcode}")
        y -= 20
        p.drawString(100, y, f"Views: {listing.views}")
        y -= 20
        p.drawString(100, y, f"Is Available: {listing.is_available}")
        y -= 20
        p.drawString(100, y, f"Created At: {listing.created_at}")
        y -= 20
        p.drawString(100, y, f"Updated At: {listing.updated_at}")
        y -= 20
        p.drawString(100, y, f"Description: {listing.description}")
        y -= 20

        # Add a page break after each listing
        p.showPage()

    # Close the PDF
    p.save()

    return response

def requestReport(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="view_requests_report.pdf"'

    # Create a canvas object
    p = canvas.Canvas(response)

    # Query data from the ViewRequest model
    view_requests = ViewRequest.objects.all()

    # Set initial y position
    y = 800

    # Write the data to the PDF
    for view_request in view_requests:
        p.drawString(100, y, f"User: {view_request.user.first_name} {view_request.user.last_name}")
        y -= 20
        p.drawString(100, y, f"Listing: {view_request.listing.title}")
        y -= 20
        p.drawString(100, y, f"Message: {view_request.message}")
        y -= 20
        p.drawString(100, y, f"Timestamp: {view_request.timestamp}")
        y -= 20

        # Add a page break after each view request
        p.showPage()

    # Close the PDF
    p.save()

    return response






































# def home(request):
#     if request.method == 'POST':
#         form = PaymentForm2(request.POST)
#         message = "Form Submitted Successfully,make another payment?"
#         if form.is_valid():
#             form.save()
#             form = PaymentForm2
#             message = message

#     else:
#         form = PaymentForm2()
#         message = None

#     context = {
#         'form': form,
#         'message': message,
#     }
#     return render(request, 'base.html', context)


# def lipaNAMpesa(request):
#     lipa_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#     headers = {"Content-Type": "application/json"}
#     headers.update({'Authorization': 'Bearer {0}'.format(AccessToken.validToken)})
#     payload = {
#         "BusinessShortCode": Password.shortCode,
#         "Password": "{0}".format(Password.decodedPassword),
#         "Timestamp": "{0}".format(Password.timeStamp),
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": "1",
#         "PartyA": "254748792401",
#         "PartyB": Password.shortCode,
#         "PhoneNumber": "254748792401",
#         "CallBackURL": "https://5968-217-21-116-221.in.ngrok.io/callback-url",
#         "AccountReference": "Test",
#         "TransactionDesc": "Test"
#     }
#     response = requests.post(lipa_url, json=payload, headers=headers)
#     print(response.content)

#     return HttpResponse(response.content, content_type='application/json')


# @csrf_exempt
# def callBack(request):
#     if request.method == 'POST':
#         # Extract the callback data from the request body
#         response = request.body.decode('utf-8')
#         print(response)
#         callback_data = json.loads(response)
#         return HttpResponse(callback_data, content_type='application/json')


# def c2b(request):
#     headers = {"Content-Type": "application/json"}
#     headers.update({'Authorization': 'Bearer {0}'.format(AccessToken.validToken)})
#     url_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
#     payload = {
#         "ShortCode": 600991,
#         "ResponseType": "Completed",
#         "ConfirmationURL": "https://f27a-41-89-10-241.ngrok-free.app/confirmation",
#         "ValidationURL": "https://f27a-41-89-10-241.ngrok-free.app/validation",
#     }
#     response = requests.post(url_endpoint, headers=headers, json=payload)
#     response = response.text.encode('utf8')
#     print(response)
#     return HttpResponse(response)


# @csrf_exempt
# def confirmation(request):
#     if request.method == 'POST':
#         response = request.body.decode('utf-8')
#         print(response)
#         callback_data = json.loads(response)
#         return HttpResponse(callback_data, content_type='application/json')
#     else:
#         return HttpResponse('Invalid request method')

# @csrf_exempt
# def validation(request):
#     if request.method == 'POST':
#         response = request.body.decode('utf-8')
#         print(response)
#         callback_data = json.loads(response)
#         return HttpResponse(callback_data, content_type='application/json')
#     else:
#         return HttpResponse('Invalid request method')
