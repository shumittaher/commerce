from django import forms
from django.forms import ModelForm
from .models import Listings, Comments, Categories

class NewListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['object_name', 'category', 'object_price', 'object_description', 'picture_URL', ]
        widgets = {
            'object_name': forms.TextInput(attrs={'class':"form-control form-control-lg", 'placeholder': 'Enter Item Title'}),
            'category': forms.Select(attrs={'class':"form-control", 'required': True}),
            'object_price': forms.NumberInput(attrs={'class':"form-control", 'placeholder':"Starting Price", 'step':"0.01"}),
            'object_description': forms.Textarea(attrs={'class':"form-control", 'placeholder':"Description", 'rows': "7"}),
            'picture_URL': forms.URLInput(attrs={'class':"form-control", 'placeholder':"Picture URL"}),
        }

        labels = {
            'object_name': 'Item Name',
            'category': 'Category',
            'object_price': 'Starting Price',
            'object_description': 'Item Description',
            'picture_URL': 'Link to Picture',
        }

class Item_user_combo(forms.Form):

    item_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    
class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields= ['comment_text']

        widgets = {
            'comment_text' : forms.Textarea(attrs={'class':"form-control", 'placeholder':"Your Comment", 'rows': "7"}),
        }

        labels = {
            'comment_text': 'Comment'
        }