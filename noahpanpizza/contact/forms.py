from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(label='email', required=True)
    subject = forms.CharField(label='subject', required=True)
    message = forms.CharField(
        label='message', widget=forms.Textarea, required=True)
