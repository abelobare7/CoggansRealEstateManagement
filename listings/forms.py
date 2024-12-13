from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    

    class Meta:
        model = Listing
        exclude = ['is_available','views']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['images'].widget.attrs['multiple'] = True

class EditListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['is_available','views']
        fields = "__all__"

# class SearchListingForm(forms.ModelForm):
#     class Meta:
#         model = Listing
#         fields = ['title', 'price','status']


class ListingSearchForm(forms.Form):
    location = forms.CharField(required=False)
    bedrooms = forms.IntegerField(required=False)
    bathrooms = forms.IntegerField(required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)

class ViewRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)