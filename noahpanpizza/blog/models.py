from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import readtime
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(
        blank=True, null=True)  # unrestricted text length
    # auto_now or auto_now_add also works (with slight caviates)
    date_posted = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    readtime = models.CharField(null=True, blank=True, max_length=100)

    # Defines where to redirect the user when a post is created with the
    # PostCreateView
    def get_absolute_url(self):
        return reverse(
            "post-detail",
            kwargs={
                "pk": self.pk,
                "slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.readtime = str(readtime.of_text(self.title + self.content))
        if self.slug is None:
            mslug = slugify(self.title)
            exists = Post.objects.filter(slug=mslug).exists()
            count = 1
            while exists:
                count += 1
                mslug = slugify(self.title) + "-" + str(count)
                exists = Post.objects.filter(slug=mslug).exists()
            self.slug = mslug
        super().save(*args, **kwargs)
