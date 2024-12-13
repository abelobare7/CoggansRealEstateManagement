from django.shortcuts import render, redirect
from .models import *
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail


def property_inquiry(request, property_id):
    property = Property.objects.get(id=property_id)

    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property
            inquiry.user = request.user
            inquiry.save()
            # Send email to the landlord about the inquiry

            return redirect('inquiry_success')  # Redirect to a success page
    else:
        form = PropertyInquiryForm()

    context = {
        'form': form,
        'property': property,
    }
    return render(request, 'tenantMngt/property_inquiry.html', context)


def viewTenants(request):
    user = request.user
    listing = Listing.objects.filter(landlord=user)
    tenants = Tenant.objects.filter(listing=listing)
    context = {
        "tenants":tenants,
        'listing':listing
        }
    return render(request, 'landlordManager/dashboard.html', context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone_number"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            #send mail to admin with the details of query submitted by tenant
            send_mail(
                subject='New Contact Message: ' + subject,
                message=f'Name: {name}\nEmail: {email}\nPhone Number: {phone}\n\nMessage: {message}',
                from_email=email,
                recipient_list=["abelgithub@gmail.com"],
                fail_silently=False,
            )
            form.save()
            messages.success(request, "Message sent successfully", extra_tags='success')
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        "form":form
    }
    return render(request, 'contacts/contact.html', context)