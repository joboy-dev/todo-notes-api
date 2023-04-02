from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.utils import timezone

from .manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    profile_pic = models.ImageField(default='profile_pics/default.PNG', upload_to='profile_pics', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email