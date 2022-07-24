from django.db import models
from django.contrib.auth.models import AbstractUser


class ApiUser(AbstractUser):
	username = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)

	ROLE = (('N', 'Normal User'), ('A', 'Admin'))
	role = models.CharField(max_length=1, choices=ROLE, default='N')
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['password']



