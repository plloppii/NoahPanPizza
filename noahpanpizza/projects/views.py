from django.shortcuts import render, redirect
from projects.models import Project
from taggit.models import Tag
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import CreateProjectForm
# Create your views here.


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    ordering = ["-date_posted"]

    def get_queryset(self):
        if "active" in self.kwargs and self.request.user.is_authenticated:
            return Project.objects.filter(active=False)
        return Project.objects.filter(active=True)


class ProjectTagView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    ordering = ["-date_posted"]

    def get_queryset(self):
        tags = Tag.objects.filter(slug=self.kwargs.get(
            'tagslug')).values_list('name', flat=True)
        return Project.objects.filter(tags__name__in=tags)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProjectDetailView(DetailView):
    model = Project


class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    # fields = ['title', 'project_type', 'description', 'content', 'images']
    form_class = CreateProjectForm
    success_url = reverse_lazy("projects")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if "post" in request.POST:
                post = self.request.POST.copy()
                post['active'] = ['on']
                form = self.form_class(post, request.FILES)
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = CreateProjectForm

    def post(self, request, *args, **kwargs):
        if "post" in self.request.POST:
            post = self.request.POST.copy()
            post['active'] = ['on']
            self.request.POST = post
        return super().post(request)


class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    success_url = '/projects'
