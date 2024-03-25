from django.db import models
from django.conf import settings
from uuid import uuid4
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Name must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Name must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    email_is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']
    objects = CustomUserManager()


    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PasswordResetToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class EmailComfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Userdata(models.Model):
    """
    example('U1','I do', '<img>', 'M', '2024-02-26 21:07UTC-8'
            '2010-08-21',
            'true', 'https://www.instagram.com/p/CxPC67MS7nx/',
            'https://www.facebook.com/tuntundragon/',
            'https://snapchat.com/add/u1',
            'http://localhost:8000/invite/U1',
            'root1234'
            )
    """
    Gender_CHOICES = [
        ("M", "Cis Gender Male"),
        ("F", "Cis Gender Female"),
        ("N", "Non Binary"),
        ("NA", "Prefer Not To Say")
    ]
    username = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    headshot = models.ImageField(upload_to='img/headshots/', null=True, default='img/headshots/default.png')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    #hard coded gender customizable gender TBD
    gender = models.CharField(choices=Gender_CHOICES)
    date_of_birth = models.DateField()
    show_horoscope = models.BooleanField(default=True)
    #social media links
    instagram_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    snapchat_link = models.URLField(null=True, blank=True)

    inviteurl = models.URLField()

    def __str__(self):
        return '%s' % (self.username)

class Connection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    #inviter user id
    inviter = models.ForeignKey(Userdata, related_name='inviter_connections', on_delete=models.CASCADE)
    #invitee user id
    invitee = models.ForeignKey(Userdata, related_name='invitee_connections', on_delete=models.CASCADE)
    date_established = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    #hard coded closeness level
    closeness = models.CharField(max_length=20, choices=[
        ('friend', 'Friend'),
        ('closefriend', 'Close Friend'),
        ('bestfriend', 'Best Friend'),
    ])
    nicknamechildtoparent = models.CharField(max_length=64, null=True)
    nicknameparenttochild = models.CharField(max_length=64, null=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inviter} invited {self.invitee}"

