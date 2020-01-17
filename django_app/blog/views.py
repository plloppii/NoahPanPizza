from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post
from django.contrib.auth.models import User

def home(request):
	context = { 
		"posts" : Post.objects.all()
	}
	return render(request, 'blog/home.html', context) #context will be avalible in templates

def about(request):
	# context = {
	# 	'title': 'Title of the about page'
	# }
	return render(request, 'blog/about.html', { 'title':'about' })
