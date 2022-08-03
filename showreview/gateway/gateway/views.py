import requests
import jwt
import json
from jwt.exceptions import DecodeError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from django.conf import settings
from .models import Api
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "service not available, try again later."
    default_code = "service_unavailable"


class UrlError(APIException):
    status_code = 503
    default_detail = "Please enter a valid url, try again later."
    default_code = "Bad URL"


CACHE_TTL = getattr(settings, "CACHE_TTL")


def get_username(token):
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except DecodeError:
        raise AuthenticationFailed("Token is invalid")

    return payload["usr"]


def check_cache(token):
    username = get_username(token)
    if username in cache:
        if cache.get(username) == token:
            return True
        else:
            return False
    else:
        return False


def save_token(token):
    username = get_username(token)
    cache.set(username, token, CACHE_TTL)


def get_relative_url(url):
    path = url.split("/")
    requested_service = "/".join(path[2:])

    return requested_service


def get_desired_api(service):
    api = Api.objects.filter(name=service).first()
    if not api:
        raise ServiceUnavailable

    return api


def validate_token(token):
    if not check_cache(token):
        headers = {"content-type": "application/json", "JWT": token}
        user_api = Api.objects.filter(name="user").first()
        url = user_api.main_url + "user/verify/"

        resp = requests.post(url, headers=headers, timeout=2.50)
        print(resp.status_code == 200)
        if resp.status_code == 200:
            save_token(token)
            return True
        else:
            return False
    else:
        return True


class Routing(APIView):
    def send(self, request):
        requested_service = get_relative_url(request.get_full_path())
        service = requested_service.split("/")[0]
        api = get_desired_api(service)

        token = request.META.get("HTTP_JWT", "")

        if token:
            if not validate_token(token):
                return Response(
                    {"detail": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST
                )

        resp = api.handle_request(request, requested_service, token)

        if resp.headers.get("Content-Type", "").lower() == "application/json":
            data = resp.json()
        else:
            data = resp.content

        return Response(data=data, status=resp.status_code)

    def get(self, request):
        return self.send(request)

    def post(self, request):
        return self.send(request)

    def delete(self, request):
        return self.send(request)

    def put(self, request):
        return self.send(request)
