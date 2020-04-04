

python3 manage.py shell

from blog.models import Post
from django.contrib.auth.models import User
users = Users.objects.all()
with open("posts.json") as f: data = json.load(f)
for item in data:
    new_post = Post(title = item["title"], content = item["content"], author = User.objects.get(id = tmp["user_id"]))
    new_post.save()