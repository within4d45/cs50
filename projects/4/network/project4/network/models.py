from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # We have to add 'symmetrical=False' because it is possible that one User follows another
    # one without being followed back.
    following = models.ManyToManyField("self", related_name='followers', symmetrical=False)

class Post(models.Model):
    content = models.CharField(max_length=1028)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.IntegerField(default = 0)
    
    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.timestamp}"
    