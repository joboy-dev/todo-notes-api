from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'user_app'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('update/', views.UpdateDetailsView.as_view(), name='update-details'),
    path('uploadPicture/', views.UploadProfilePictureView.as_view(), name='upload-picture'),
    path('changePassword/', views.ChangePasswordView.as_view(), name='change-password')
]