from django.db import models
from django.contrib.auth.models import User

from user.models import CustomUser

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=50000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title} -- {self.author}'