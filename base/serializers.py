from rest_framework import serializers
from .models import CustomUser as Userr
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
import json
from dataclasses import field
from rest_framework import serializers
from string import ascii_lowercase, ascii_uppercase
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .utils import *










class PostSerializer(serializers.ModelSerializer):



    user_avi = serializers.ImageField(read_only=True)
    user_name = serializers.CharField(read_only=True)




    class Meta:
        model = Post
        fields = '__all__' 





    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

        return post
        

        



# Change FolllowersSerializer to FollowersSerializer
    







class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
   


    




    class Meta:
        model = Userr
        fields = '__all__'



    def get__id(self, obj):
        return obj.id
    
    def get_isAdmin(self, obj):
        return obj.is_staff

        
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name
    
    def get_bio(self, obj):
        bio = obj.bio


        return bio
    
    def get_avi(self, obj):
        avi = obj.avi


        return avi


    def get_date_joined(self, obj):
        date_joined = obj.date_joined


        return date_joined
    


from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import jwt
from pytz import timezone  # Import timezone from pytz
from datetime import timedelta


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    expiration_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Userr
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'bio', 'token' , 'expiration_time' , 'avi']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    def get_expiration_time(self, obj):
        token = RefreshToken.for_user(obj)
        access_token = str(token.access_token)
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})  # Decode token without verification
        expiration_timestamp = decoded_token['exp']  # Get the expiration time from the decoded token
        expiration_datetime_utc = datetime.utcfromtimestamp(expiration_timestamp)  # Convert expiration timestamp to UTC datetime
        expiration_datetime_local = expiration_datetime_utc.astimezone(timezone('Africa/Nairobi'))  # Convert to Nairobi timezone
        expiration_datetime_local += timedelta(hours=3)  # Add three hours to the expiration time
        return expiration_datetime_local.strftime('%Y-%m-%d %H:%M:%S %Z')  # 

    






from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from base.utils import send_normal_email


class MessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    unread_count = serializers.SerializerMethodField()


    class Meta:
        model = Message
        fields = ["sender", "receiver", "content", "timestamp", "is_read", "name", "unread_count"]

    def get_unread_count(self, obj):
        # Assuming obj.sender and obj.receiver are instances of CustomUser
        return Message.get_unread_count(obj.sender, obj.receiver)



