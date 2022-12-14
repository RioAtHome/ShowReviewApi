import requests, json
from requests.exceptions import ConnectionError
from django.db import models
from rest_framework.response import Response


class Api(models.Model):
    name = models.CharField(max_length=64, unique=True)
    main_url = models.URLField(max_length=255, unique=True)

    def handle_request(self, request, relative_url, token=None):
        headers = {}
        if token:
            headers["JWT"] = token

        full_path = self.main_url + relative_url
        method = request.method.lower()

        mapping_methods = {
            "get": requests.get,
            "post": requests.post,
            "patch": requests.patch,
            "delete": requests.delete,
        }

        if request.content_type and request.content_type.lower() == "application/json":
            data = json.dumps(request.data)
            headers["content-type"] = request.content_type

        else:
            data = request.data
        try:
            resp = mapping_methods[method](full_path, headers=headers, data=data)
        except ConnectionError:
            resp = Response(headers=headers, data=data, status=404)

        return resp

    def __str__(self):
        return self.name
