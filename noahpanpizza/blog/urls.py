from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # path('', views.home, name= 'blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('archive', PostListView.as_view(), {"active": False}, name='blog-archive'),
    path('<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'), #pk= primarykey
    path('new/',PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/<slug:slug>/update/',PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/<slug:slug>/delete/',PostDeleteView.as_view(), name='post-delete'),
]

#Class based views look for the following template naming convention
#<app>/<model>_<viewtype>.html