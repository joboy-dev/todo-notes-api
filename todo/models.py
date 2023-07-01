from django.db import models
from django.contrib.auth.models import User

from user.models import CustomUser

import datetime

class Todo(models.Model):
    name = models.CharField(max_length=100)
    # content = models.CharField(max_length=1000)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.date.today)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    class Meta:
        ordering = ['-due_date']
        
    def __str__(self):
        return f'{self.name} -- {self.due_date}'
