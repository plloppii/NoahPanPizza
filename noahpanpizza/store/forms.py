from django import forms
from django_countries.fields import CountryField

PAYMENT_OPTIONS = [
    ('CC', 'Credit Card'),
    ('S', 'Stripe'),
    ('P', 'Paypal')
]


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), label="")
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name'}),
        label="")
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email Address'}),
        label="")
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}), label="")
    address1 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Address 1'}), label="")
    address2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Address 2 (Optional)'}),
        required=False,
        label="")
    country = CountryField(blank_label="Select Country").formfield(label="")
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'State'}),
        label="")
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City'}),
        label="")
    zipcode = forms.CharField(
        max_length=5,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Zip'}),
        label="")
    same_billing_address = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False, initial=True)


class ContactForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), label="")
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name'}),
        label="")
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email Address'}),
        label="")
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}), label="")


class ShippingForm(forms.Form):
    address1 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Address 1'}), label="")
    address2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Address 2 (Optional)'}),
        required=False,
        label="")
    country = CountryField(blank_label="Select Country").formfield(label="")
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'State'}),
        label="")
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City'}),
        label="")
    zipcode = forms.CharField(
        max_length=5,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Zip'}),
        label="")
    same_billing_address = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False, initial=True)
