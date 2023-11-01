from django.forms import ModelForm
from .models import Userdetails
from django import forms
from .models import Service
class Userform(ModelForm):
    class Meta:
        model=Userdetails
        fields= [
             "full_name",
             "email",
             "phone",
             "username" ,
             "password",
        ]

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']

