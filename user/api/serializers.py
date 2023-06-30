from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):

    '''Serializer than handles user creation'''

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'password2', 'profile_pic']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        read_only_fields = ['id', 'profile_pic']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error': 'Your passwords do not match. Try again'})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'A user is registered with this email'})
        
        # validate password
        validate_password(data['password'])
        
        return data
        
    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        # profile_pic = validated_data.get('profile_pic')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            # profile_pic=profile_pic,
        )

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user
    

class LoginSerializer(serializers.Serializer):

    '''Serializer than handles user login'''

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        # authenticate user
        user = authenticate(email=data['email'], password=data['password'])

        # check if user exists
        if user is None:
            raise serializers.ValidationError({'error': 'This user does not exist'})
        
        # remove items not to vbe shown in response
        email = data.pop('email')
        data.pop('password')
        
        token = Token.objects.get_or_create(user=user)

        data['response'] = f'Welcome {email}'
        data['token'] = token[0].key
        data['id'] = user.pk

        return data


class UpdateDetailsSerializer(serializers.ModelSerializer):

    '''Serializer to update user details'''

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_pic']
        read_only_fields = ['id', 'profile_pic']

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # save instance
        instance.save()

        # return instance
        return instance


class UploadProfilePictureSerializer(serializers.ModelSerializer):

    '''Serializer to upload profile picture'''

    class Meta:
        model = User
        fields = ['profile_pic']

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # save instance
        instance.save()

        # return instance
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    '''
        Serializer to change user password
    '''

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def update(self, instance, validated_data):
        email = validated_data.get('email')
        old_password = validated_data.get('password')
        new_password = validated_data.get('new_password')
        confirm_password = validated_data.get('confirm_password')

        user = authenticate(email=email, password=old_password)

        if user is None:
            raise serializers.ValidationError({'message': 'User credentials incorrect. Check your email and password and try again.'})
        elif old_password == new_password:
            raise serializers.ValidationError({'message': 'New password cannot be the same as old password.'})
        elif new_password != confirm_password:
            raise serializers.ValidationError({'message': 'New password and confirm password field has to be the same.'})
        
        validate_password(new_password)
        instance.set_password(new_password)

        instance.save()

        return instance
    