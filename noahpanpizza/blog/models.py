from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField() #unrestricted text length
	date_posted = models.DateTimeField(default=timezone.now) #auto_now or auto_now_add also works (with slight caviates)
	author = models.ForeignKey(User, on_delete = models.CASCADE) #on_delete-> delete post if author is deleted,
	
	# Defines where to redirect the user when a post is created with the PostCreateView
	def get_absolute_url(self):
		return reverse("post-detail", kwargs={"pk": self.pk})
	
	def __str__(self):
		return self.title

