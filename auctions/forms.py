from django import forms
from django.forms import ModelForm
from .models import Listings

# class ListingForm(forms.Form):

#     object_name = forms.CharField(label="Item Title", required=True, widget=forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Enter Item Title'}))

#     # <div class="form-group">
#     #     <input class="form-control" type="number" name="object_price" placeholder="Starting Price" step="0.01">
#     # </div>

#     # <div class="form-group">
#     #     <textarea class="form-control" name="object_description" placeholder="Description" rows="7"></textarea>
#     # </div>
    
#     # <div class="form-group">
#     #     <input class="form-control" name="picture_URL" placeholder="Picture URL">
#     # </div>

class NewListingForm(ModelForm):

    class Meta:
        model = Listings
        fields = ['object_name', 'object_price', 'object_description', 'picture_URL']
        widgets = {
            'object_name': forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Enter Item Title'}),
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

