from django import forms
from .models import AuctioningListing
from django.utils import timezone

class AuctioningListingForm(forms.ModelForm):
    class Meta:
        model = AuctioningListing
        fields = ['title', 'description', 'starting_bid', 'end_date', 'category', 'image']
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter auction title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter detailed description'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting bid'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        starting_bid = cleaned_data.get('starting_bid')
        end_date = cleaned_data.get('end_date')

        # Custom validation logic
        if starting_bid is not None and starting_bid <= 0:
            self.add_error('starting_bid', 'Starting bid must be greater than 0.')

        # Auction end date should be in the future
        if end_date is not None and end_date <= timezone.now():
            self.add_error('end_date', 'Auction end date must be in the future.')

        return cleaned_data
