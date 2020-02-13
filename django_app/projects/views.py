from django.shortcuts import render
from projects.models import Project

# Create your views here.


def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': Project.objects.all()
    }

    return render(request, 'projects/projects.html', context)
