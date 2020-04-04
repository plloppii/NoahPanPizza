from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100) #unrestricted text length
    date_posted = models.DateTimeField(default=timezone.now) #auto_now or auto_now_add also works (with slight caviates)
    project_type = models.CharField(default='',max_length=100)
    images = models.ImageField(default='', upload_to='project_pics', blank=True)
    content = models.TextField(default='')

    # Defines where to redirect the user when a post is created with the PostCreateView
    # def get_absolute_url(self):
    # 	return reverse("post-detail", kwargs={"pk": self.pk})
    def __str__(self):
        return self.title
