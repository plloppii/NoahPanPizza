from django.urls import path
from . import views
from .views import ProjectCreateView

urlpatterns = [
    path('', views.projects, name= 'projects'),
    path('new/', ProjectCreateView.as_view(), name='project-create'),
]

#Class based views look for the following template naming convention
#<app>/<model>_<viewtype>.html