from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    num_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.body} by {self.user} created on {self.timestamp.strftime('%b %d %Y, %I:%M %p')}."