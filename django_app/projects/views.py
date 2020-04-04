from django.shortcuts import render
from projects.models import Project
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
)
from .forms import CreateProjectForm
# Create your views here.

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'projects/project_list.html', context)

class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    ordering = ["-date_posted"]


class ProjectDetailView(DetailView):
    model = Project
class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    # fields = ['title', 'description', 'project_type', 'content', 'images']
    form_class = CreateProjectForm
    template_name = "projects/create_project.html"
    success_url = reverse_lazy("projects")

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(self.success_url)
    #     else:
    #         return render(request, self.template_name, {'form': form})


    # def form_valid(self, form):
    #     obj = form.save(commit= False)
    #     obj.save()




    

    
