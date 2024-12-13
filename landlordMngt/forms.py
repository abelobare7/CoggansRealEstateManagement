from .models import *
from accounts.models import *
from django import forms
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'phone_number',]