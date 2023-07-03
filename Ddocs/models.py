from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email,  username, password=None,**extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('blocked_user', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError((
                'Super user must have is_staff'
            ))

        return self.create_user(email,username,password,**extra_fields)


class User(AbstractUser):
   
    ip_address=models.CharField(max_length=100)
    blocked_user=models.BooleanField(default=False)
    permanent_blocked=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class RequestedAttempts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RequestedAttempts"
        verbose_name_plural = "RequestedAttemptss"

    def __str__(self):
        return self.user.email
