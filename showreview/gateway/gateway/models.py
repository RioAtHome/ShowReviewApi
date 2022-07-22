from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Api(AbstractUser):
	apikey = models.CharField(max_length=32, unique=True)
	name = models.CharField(max_length=32, unique=True)
	api_path = models.CharField(max_length=255)
	main_url = models.CharField(max_length=255)
	
	def __str__(self):
		return self.name

