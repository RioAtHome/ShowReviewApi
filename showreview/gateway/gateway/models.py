import requests, json
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Api(models.Model):
    name = models.CharField(max_length=64, unique=True)
    main_url = models.CharField(max_length=255)


    def handle_request(self, request):
        headers = {}
        path = request.get_full_path().split('/')
        relative_path = '/'.join(path[4:])
        full_path = self.main_url + relative_path
        method = request.method.lower()

        mapping_methods = {
            'get': requests.get,
            'post': requests.post,
        }

        if request.content_type and request.content_type.lower()=='application/json':
            data = json.dumps(request.data)
            headers['content-type'] = request.content_type
        else:
            data = request.data

        return method_map[method](url, headers=headers, data=data)


    def __str__(self):
        return self.name