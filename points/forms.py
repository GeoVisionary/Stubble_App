from django import forms
from .models import Point

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['geolocation', 'date', 'city', 'state', 'length', 'width', 'fire_status', 'image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': False}),
        }
