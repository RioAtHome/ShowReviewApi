import requests, json, jwt
from jwt.exceptions import DecodeError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from .models import Api


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


class Routing(APIView):
    def send(self, request):
        request_path = request.get_full_path()
        if request_path[-1] != "/":
            request_path += "/"

        path = request_path.split("/")
        if len(path) < 2:
            return Response("bad request", status=status.HTTP_400_BAD_REQUEST)

        api = Api.objects.filter(name=path[2]).first()
        user_api = Api.objects.filter(name="user").first()

        if api is None:
            return Response("bad request", status=status.HTTP_400_BAD_REQUEST)

        token = request.META.get("HTTP_JWT", "")
        requested_service = "/".join(path[2:])

        if not token:
            pass
        else:
            if not check_cache(token):
                headers = {"content-type": "application/json", "JWT": token}
                api = Api.objects.filter(name="user").first()
                url = user_api.main_url + "user/verify/"

                resp = requests.post(url, headers=headers, timeout=2.50)

                if resp.status_code == 200:
                    save_token(token)
                else:
                    return Response(
                        "Token is invalid", status=status.HTTP_400_BAD_REQUEST
                    )
        api = Api.objects.filter(name=path[2]).first()
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

    def update(self, request):
        return self.send(request)
