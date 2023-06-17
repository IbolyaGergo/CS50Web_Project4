from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", null=True, related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", null=True, related_name="liked_posts")
    num_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.body} by {self.user} created on {self.timestamp.strftime('%b %d %Y, %I:%M %p')}."