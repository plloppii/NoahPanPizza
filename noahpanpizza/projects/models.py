from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from taggit_autosuggest.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300) 
    content = RichTextUploadingField(blank=True, null=True)
    thumbnail = models.ImageField(default='', upload_to='project_thumbnails', blank=True)
    date_posted = models.DateTimeField(default=timezone.now) #auto_now or auto_now_add also works (with slight caviates)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    tags = TaggableManager(blank=True)
    
    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk, "slug": self.slug})

    # Defines where to redirect the user when a post is created with the PostCreateView
    # def get_absolute_url(self):
    # 	return reverse("post-detail", kwargs={"pk": self.pk})
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        mslug = slugify(self.title)
        if self.slug == None or self.slug != mslug:
            exists = Project.objects.filter(slug=mslug).exists()
            count = 1
            while exists:
                count+=1
                mslug = slugify(self.title)+ "-"+str(count)
                exists = Project.objects.filter(slug=mslug).exists()
            self.slug = mslug
        super().save(*args, **kwargs)