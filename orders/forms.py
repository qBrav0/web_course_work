from django import forms
from .models import Order
from django.contrib.auth.models import User

class OrderCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), initial=User.objects.get(username='Anonymous'), widget=forms.HiddenInput())
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

