from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from . import serializers

User = get_user_model()

# Create your views here.
class RegistrationView(generics.CreateAPIView):

    '''View to register users'''

    serializer_class = serializers.CreateUserSerializer
    # parser_classes = [MultiPartParser]
    queryset = User.objects.all()
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class LoginView(generics.GenericAPIView):

    '''View to login users'''

    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):

    '''View to log out users'''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get current user
        current_user = request.user

        # get current user token
        user_token = Token.objects.get(user=current_user)
        user_token.delete()

        return Response({'message': 'Logged out successfully'})
    

class UpdateDetailsView(generics.RetrieveUpdateAPIView):

    '''View to update user details'''

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UpdateDetailsSerializer

    def get_queryset(self):
        current_user = self.request.user

        return User.objects.filter(pk=current_user.pk)
    
    def get_object(self):
        return self.request.user
    

class UploadProfilePictureView(generics.RetrieveUpdateAPIView):

    '''View to upload profile picture'''

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = serializers.UploadProfilePictureSerializer

    def get_queryset(self):
        current_user = self.request.user

        return User.objects.filter(pk=current_user.pk)

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.RetrieveUpdateAPIView):
    '''
        View to change user password
    '''

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(pk=current_user.pk)

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({'message': 'Password change successful'})
