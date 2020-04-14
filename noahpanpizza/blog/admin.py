from django.contrib import admin
from .models import Post


admin.site.register(Post)
# adding the Post DB to the Admin site. 
# Post is a inheriting the models class in django.db
