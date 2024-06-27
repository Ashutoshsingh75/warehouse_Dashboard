from datetime import datetime
from pyexpat import model
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms.widgets import Widget
from .models import LaundryUser,LaundryshopeUser,Laundrytype,Order_details
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm


class DateTimeInput(forms.DateTimeInput):
    input_type='datetime-local'





class Signup(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    retype_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=LaundryUser
        fields="__all__"

    def clean(self):
        super().clean()
        p=self.cleaned_data.get('password')
        p1=self.cleaned_data.get('retype_password')
        if p!=p1 or len(p)<6:
            raise forms.ValidationError("Error password : Both Password did not match...")



class userlogin(forms.Form):
    email=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        email=self.cleaned_data.get("email")
        passw=self.cleaned_data.get("password")
        try:
            userdata=LaundryUser.objects.get(email=email)
        except:
            raise forms.ValidationError("User Does Not Exits")
        else:
            if not check_password(passw,userdata.password):
                raise forms.ValidationError("Password does not match")

class lundey_user(forms.ModelForm):
    class Meta:
        model=LaundryshopeUser
        exclude = ('name',) 

class lundey_cat(forms.ModelForm):
    class Meta:
        model=Laundrytype
        exclude = ('user',) 


class pay(forms.ModelForm):
    class Meta:
        model=Order_details
        fields=["payment"]


class profile(forms.ModelForm):
    class Meta:
        model=LaundryUser
        exclude =('password',)

class oderformforupdate(forms.ModelForm):
    class Meta:
        model=Order_details
        fields=["status","payment","delivery_date"]
        widgets = {
        'delivery_date':DateTimeInput()
        }

class shopform(forms.ModelForm):
    class Meta:
        model=LaundryshopeUser
        fields="__all__"
        