from django import forms
from django_countries.fields import CountryField

class CheckoutForm(forms.Form)
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.CharField(label="Email Address")
    address1 = forms.CharField()
    address2 = forms.CharField()
    country = CountryField(blank_label="Select Country")
    zipcode = forms.CharField(max_length=5, default="11222")
    same_for_billing = forms.BooleanField(default=False)
    
