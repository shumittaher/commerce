from django import forms
from django.forms import ModelForm
from .models import Listings

class NewListingForm(ModelForm):

    class Meta:
        model = Listings
        fields = ['object_name', 'object_price', 'object_description', 'picture_URL']
        widgets = {
            'object_name': forms.TextInput(attrs={'class':"form-control form-control-lg", 'placeholder': 'Enter Item Title'}),
            'object_price': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Starting Price", 'step':"0.01"}),
            'object_description': forms.Textarea(attrs={'class':"form-control", 'placeholder':"Description", 'rows': "7"}),
            'picture_URL': forms.URLInput(attrs={'class':"form-control", 'placeholder':"Picture URL"})
        }

        labels = {
            'object_name': 'Item Name',
            'object_price': 'Starting Price',
            'object_description': 'Item Description',
            'picture_URL': 'Link to Picture'
        }

class Item_user_combo(forms.Form):

    item_id = forms.IntegerField()
    user_id = forms.IntegerField()
    

