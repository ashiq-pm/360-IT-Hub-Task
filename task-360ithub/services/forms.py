from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'payment_terms', 'service_price', 'service_package', 'service_tax', 'service_image', 'active']
        
        widgets = {
            'service_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service name'
            }),
            'payment_terms': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payment terms'
            }),
            'service_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service price'
            }),
            'service_package': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service package'
            }),
            'service_tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service tax percentage'
            }),
            'service_image': forms.ClearableFileInput(attrs={
                'class': 'file-input'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class SubscriptionForm(forms.Form):
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your address',
            'class': 'custom-textarea'
        }),
        label="" 
    )