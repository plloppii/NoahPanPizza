from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name= 'projects'),
]

#Class based views look for the following template naming convention
#<app>/<model>_<viewtype>.html