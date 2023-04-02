from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extras):
        # check if there is a value in the email
        if not email:
            raise ValueError(gettext_lazy('Email field is required'))
        
        # normalize email so dmmain name is automatically small letter eg Joseph@gmail.com will be joseph@gmail.com 
        email = self.normalize_email(email)
        # pass in values into the user model
        user = self.model(email=email, **extras)
        # set password
        user.set_password(password)
        # save user instance
        user.save()

        # return user instance
        return user

    def create_superuser(self, email, password, **extras):
        # set default values
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_active', True)

        # check if extras for staff and superuser have values that is true since this is a superuser
        if extras.get('is_staff') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_staff=True'))
        if extras.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_superuser=True'))
        
        # create user
        return self.create_user(email, password, **extras)
