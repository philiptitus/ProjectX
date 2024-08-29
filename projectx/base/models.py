from django.db import models
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from base.validators import file_size
from decimal import Decimal
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter a valid email address"))

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

from django.db import models




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avi = models.ImageField(null=True, blank=True, default='/avatar.png')
    isPrivate = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)



    objects = CustomUserManager()
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
    
    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }


from django.db import models
from django.conf import settings
from decimal import Decimal

class Post(models.Model):
    caption = models.CharField(max_length=50)
    description = models.TextField(max_length=264)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    isSlice = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    location = models.CharField(max_length=100, blank=True, null=True)  # New location field

    @property
    def user_avi(self):
        return self.user.avi if self.user else None

    @property
    def user_name(self):
        return self.user.email if self.user else None

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['-created_date']


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "albums")
    album = models.ImageField( null=True, blank=True)


class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "videos")
    video=models.FileField(validators=[file_size])

        



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)


    @property
    def comment_avi(self):
        return self.user.avi if self.user else None
    
    @property
    def comment_email(self):
        return self.user.email if self.user else None


    def __str__(self):
        return self.message
    

    class Meta:
        ordering = ['-created_at']




from django.db.models import Q


class Message(models.Model):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    @property
    def name(self):
        return self.sender.username if self.sender else None

    @classmethod
    def get_unread_count(cls, user1, user2):
        """
        Get the total number of unread messages between two users.
        """
        unread_count = cls.objects.filter(
            Q(sender=user1, receiver=user2, is_read=False) |
            Q(sender=user2, receiver=user1, is_read=False)
        ).count()
        return unread_count

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content}'
