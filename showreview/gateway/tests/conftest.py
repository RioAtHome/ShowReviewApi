import pytest
import requests
from gateway.models import Api
from rest_framework.response import Response
import os
import django
from django.conf import settings

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gateway.ApiGateway.settings')


def pytest_configure():
    settings.DEBUG = False
    # If you have any test specific settings, you can declare them here,
    # e.g.
    # settings.PASSWORD_HASHERS = (
    #     'django.contrib.auth.hashers.MD5PasswordHasher',
    # )
    django.setup()


@pytest.fixture
def disable_network_calls(monkeypatch):
    def stunted_get(*args, **kwargs):
        data = kwargs["data"]
        headers = kwargs["headers"]

        return Response(data=data, headers=headers, status=200)

    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: stunted_get(*args, **kwargs)
    )
    monkeypatch.setattr(
        requests, "post", lambda *args, **kwargs: stunted_get(*args, **kwargs)
    )
    monkeypatch.setattr(
        requests, "delete", lambda *args, **kwargs: stunted_get(*args, **kwargs)
    )
    monkeypatch.setattr(
        requests, "put", lambda *args, **kwargs: stunted_get(*args, **kwargs)
    )


@pytest.fixture
def fake_validation(monkeypatch):
    def fake_response(*args, **kwargs):

        return Response(status=200)

    monkeypatch.setattr(
        requests, "post", lambda *args, **kwargs: fake_response(*args, **kwargs)
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_data():
    Api(1, "sth", "https://www.testtheurl.com/").save()
    Api(2, "sth2", "Http://www.woowthisisatest.com/").save()
    Api(2, "user", "http://www.authenticate.com/").save()
