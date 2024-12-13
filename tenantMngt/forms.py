from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email', 'phone_number','subject','message']

class ListingInquiryForm(forms.ModelForm):
    class Meta:
        model = PropertyInquiry
        fields = '__all__'