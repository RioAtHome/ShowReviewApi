from django.db import models
from django.contrib.auth.models import User


class ApiUser(models.Model):
	ROLE = (('N', 'Normal user'), ('A', 'Admin'))
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=1, choices=ROLE, default='N')


