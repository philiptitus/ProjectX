from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from pusher import Pusher
from base.utils import *
from rest_framework import generics
from ..serializers import *
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import CustomUser  as Userr
from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from base.serializers import *
# Create your views here.

from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.conf import settings




        

from typing import Dict, Any


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer








    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from django.db.models import Q






from django.db.models import Case, When, Value, IntegerField

from django.db.models import Q, F
from rest_framework.pagination import PageNumberPagination



from django.contrib.auth.validators import UnicodeUsernameValidator

class RegisterUser(APIView):

    def post(self, request):
        data = request.data

        # Check password length
        if len(data['password']) < 8:
            content = {'detail': 'Password must be at least 8 characters long.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Check password for username and email
        username_validator = UnicodeUsernameValidator()
        if username_validator(data['password']):
            content = {'detail': 'Password cannot contain username or email.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Check for minimum number of upper and lowercase characters
        uppercase_count = sum(1 for c in data['password'] if c.isupper())
        lowercase_count = sum(1 for c in data['password'] if c.islower())
        if uppercase_count < 1 or lowercase_count < 1:
            content = {'detail': 'Password must contain at least one uppercase and lowercase character.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Check for minimum number of digits and special characters
        digit_count = sum(1 for c in data['password'] if c.isdigit())
        special_count = sum(1 for c in data['password'] if not c.isalnum())
        if digit_count < 1 or special_count < 1:
            content = {'detail': 'Password must contain at least one digit and one special character.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            user = Userr.objects.create_user(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=data['password'],
            )





        except IntegrityError:
            message = {'detail': 'User with this email already exists.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    




@permission_classes([IsAuthenticated]) 
class GetUserProfile(APIView):

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)


        return Response(serializer.data)
    

@permission_classes([IsAuthenticated])
class UpdateUserProfile(APIView):

    def put(self, request):
        user = request.user
        serializer = UserSerializerWithToken(user, many=False)
        data = request.data

        # Update password if provided
        if 'password' in data and data['password'] != '':
            # Add password strength checks here
            if len(data['password']) < 8:
                content = {'detail': 'Password must be at least 8 characters long.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            uppercase_count = sum(1 for c in data['password'] if c.isupper())
            lowercase_count = sum(1 for c in data['password'] if c.islower())
            if uppercase_count < 1 or lowercase_count < 1:
                content = {'detail': 'Password must contain at least one uppercase and lowercase character.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            digit_count = sum(1 for c in data['password'] if c.isdigit())
            special_count = sum(1 for c in data['password'] if not c.isalnum())
            if digit_count < 1 or special_count < 1:
                content = {'detail': 'Password must contain at least one digit and one special character.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            user.password = make_password(data['password'])



        # Update user profile details
        user.first_name = data.get('name', user.first_name)
        user.username = data.get('email', user.username)
        user.email = data.get('email', user.email)
        user.bio = data.get('bio', user.bio)
        user.isPrivate = data.get('isPrivate', user.bio)




        # Save updated user profile
        user.save()

        # Return updated user data
        return Response(serializer.data)
    


@permission_classes([IsAuthenticated])
class deleteAccount(APIView):
    def delete(self, request):
        # Use request.user to get the authenticated user
        user_for_deletion = request.user



        # Delete the user
        user_for_deletion.delete()

        return Response("The user was deleted successfully")

    






from django.shortcuts import get_object_or_404





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated