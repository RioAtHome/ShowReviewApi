from django.db import models
from django.contrib.auth.models import AbstractUser


class ApiUser(AbstractUser):
	username = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)

	ROLE = ((0, 'Normal User'), (1, 'Admin'))
	role = models.BooleanField(choices=ROLE, default=0)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['password']



