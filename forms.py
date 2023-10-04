from django.forms import ModelForm
from .models import Userdetails
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