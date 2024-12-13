from django import forms
from django.core.validators import RegexValidator
import re

def validate_phone_number(value):
    if not value.startswith('+254'):
        raise forms.ValidationError('Phone number must start with +254.')

    if value.startswith('+25407'):
        # Remove the leading '0'
        value = '+254' + value[4:]

    if not re.match(r'^\+2547\d{8}$', value):
        raise forms.ValidationError('Enter a valid phone number starting with +2547.')
