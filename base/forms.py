from django import forms
from .models import *


class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=10)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class PaymentForm2(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
