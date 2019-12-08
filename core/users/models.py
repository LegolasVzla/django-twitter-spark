from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
	'''First Name and Last Name are must in POST and optionals in PUT and also
	are required in forms'''
	first_name = models.CharField( max_length = 100, null=True, blank = True)
	last_name = models.CharField( max_length = 100, null=True, blank = True)
	email = models.EmailField(_('email address'), unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)
	updated_date=models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
	    return self.email