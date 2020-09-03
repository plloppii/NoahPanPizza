from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ContactForm 
from django.views.generic import View
# Create your views here.

class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'contact/contact.html', {'form': form}) 
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject=subject, message=message, from_email=from_email, recipient_list=["noahpan323@gmail.com"])
            except BadHeaderError:
                return HttpResponse('Invalid header!')
            return redirect('/contact/success', permanent=True)
        else:
            return HttpResponse('Form Invalid. Something went wrong. Sorry!')
        return render(request, 'contact/contact.html', {'form': form}) 
