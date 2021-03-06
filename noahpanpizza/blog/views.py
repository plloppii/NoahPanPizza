from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Function based views:
# URL Pattern is directed to certain app view. These views then handle logic for the routes.
# Then finally they render the templates.


def home(request):
    context = {
        "posts": Post.objects.all()
    }
    # context will be avalible in templates
    return render(request, 'blog/post_list.html', context)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]  # order posts backwards
    # ordering = ["date_posted"]
    paginate_by = 8

    def get_queryset(self):
        if "active" in self.kwargs and self.request.user.is_authenticated:
            return Post.objects.filter(active=False)
        return Post.objects.filter(active=True)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Using default naming convension of the DetailView so we can cut down on code.


class PostDetailView(DetailView):
    model = Post


class PostCreateView(StaffRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'active', 'featured']

    def post(self, request, *args, **kwargs):
        if "post" in self.request.POST:
            post = self.request.POST.copy()
            post['active'] = ['on']
        return super().post(request)

# LoginRequired Mixin is similar to the decorators of function based views.
# It requires the user to be logged in to update the posts.
# UserPassesTestMixin calls test_func, that checks requirements.


class PostUpdateView(StaffRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'active', 'featured']

    def post(self, request, *args, **kwargs):
        if "post" in self.request.POST:
            post = self.request.POST.copy()
            post['active'] = ['on']
            self.request.POST = post
        return super().post(request)
    # Function tells who the author is of the post (who is the current user.)
    # def form_valid(self, form):
    # 	form.instance.author = self.request.user
    # 	return super().form_valid(form)
    # #test_func does not allow users to delete other peoples posts.
    # def test_func(self):
    # 	post = self.get_object()
    # 	if self.request.user == post.author:
    # 		return True
    # 	return False


class PostDeleteView(StaffRequiredMixin, DeleteView):
    model = Post
    success_url = '/blog'
    # def test_func(self):
    # 	post = self.get_object()
    # 	if self.request.user == post.author:
    # 		return True
    # 	return False


# Class based views:
# Have alot more built in functionality, that handles alot of back end logic.
# Different kinds of class based views.
# There are list views, detail views, create views, update views, delete views.
# Websites have similar functionality.
# (Blog) --> list views
# (Youtube) --> subscription views
# (Click on video or blog) --> detail views
# (Ability to update or delete views) --> update/delete views.
