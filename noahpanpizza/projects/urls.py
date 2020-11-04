from django.urls import path
from . import views
from .views import ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectDetailView, ProjectTagView

urlpatterns = [
    path('', ProjectListView.as_view(), name= 'projects'),
    path('archive/', ProjectListView.as_view(), {"active": False}, name='project-archive'),
    path('new/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/<slug:slug>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/<slug:slug>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/<slug:slug>/', ProjectDetailView.as_view(), name='project-detail'),
    path('tag/<str:tagslug>/', ProjectTagView.as_view(), name='project-tag'),
]

#Class based views look for the following template naming convention
#<app>/<model>_<viewtype>.html