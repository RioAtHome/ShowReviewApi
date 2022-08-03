import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import ApiUser
from user.requestqueue import RequestQueue


@pytest.fixture
def get_verified_user():
    client = APIClient()

    data = {"username": "rioathome", "password": "Raccon", "role": 1}

    resp = client.post(reverse("register"), data=data)

    return resp.data


@pytest.fixture
@pytest.mark.django_db
def generate_user():
    ApiUser.objects.create_user(username="mic", password="raccon", role=0).save()


@pytest.fixture
def client():
    client = APIClient()

    return client


@pytest.fixture
def fake_worker(monkeypatch):
    def response(*args, **kwargs):
        requested_data = args[1]
        username = requested_data["username"]
        data = []
        if username == "test1234":
            return data

        if requested_data["_model"] == "favorites":
            data = [
                {
                    "id": 2,
                    "username": username,
                    "created_at": "2022-08-03T05:10:05.084351Z",
                    "updated_at": "2022-08-03T05:10:05.084376Z",
                    "show": "breaking-bad",
                },
                {
                    "id": 3,
                    "username": username,
                    "created_at": "2022-08-03T05:10:17.747940Z",
                    "updated_at": "2022-08-03T05:10:17.747967Z",
                    "show": "the-walking-dead",
                },
            ]

        elif requested_data["_model"] == "reviews":
            data = [
                {
                    "id": 8,
                    "text": "This is just a test to test out things",
                    "created_at": "2022-08-03T04:17:00.014885Z",
                    "updated_at": "2022-08-03T04:17:00.014952Z",
                    "show": "the-walking-dead",
                },
                {
                    "id": 9,
                    "text": "This is just a test to test out things 123",
                    "created_at": "2022-08-03T04:17:11.959280Z",
                    "updated_at": "2022-08-03T04:17:11.959307Z",
                    "show": "the-walking-dead",
                },
            ]
        elif requested_data["_model"] == "comments":
            data = [
                {
                    "id": 3,
                    "text": "Wow, lets change this to sth else",
                    "created_at": "2022-08-03T04:19:04.696351Z",
                    "updated_at": "2022-08-03T04:19:04.696376Z",
                    "show": "the-walking-dead",
                    "review": 9,
                },
                {
                    "id": 4,
                    "text": "Wow, lets change this to sth elsasdfe",
                    "created_at": "2022-08-03T04:19:09.980777Z",
                    "updated_at": "2022-08-03T04:19:09.980804Z",
                    "show": "the-walking-dead",
                    "review": 9,
                },
            ]

        return data

    monkeypatch.setattr(
        RequestQueue, "call", lambda *args, **kwargs: response(*args, **kwargs)
    )
