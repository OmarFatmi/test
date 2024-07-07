# app/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
class UserManager(BaseUserManager):
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

class User(AbstractBaseUser):
    userId = models.CharField(max_length=100, unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

class Organisation(models.Model):
    orgId = models.CharField(max_length=36, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Ajoutez ce champ si nécessaire
    users = models.ManyToManyField('User', related_name='organisations')
    created_by = models.ForeignKey('User', related_name='created_organisations', on_delete=models.CASCADE ,null=True,default=1)

    def __str__(self):
        return self.name