from django.contrib import admin
from django.urls import path, include
from .views import ContactView 
from django.views.generic import TemplateView

urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
    path('success/', TemplateView.as_view(template_name='contact/success.html'), name='success')
]