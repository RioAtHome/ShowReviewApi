import pytest
from django.urls import reverse
from rest_framework import status
from user.models import ApiUser


@pytest.mark.django_db
def test_verify_endpoint(get_verified_user, client):
    headers = {"Content-Type": "application/json", "HTTP_JWT": get_verified_user["JWT"]}
    resp = client.post(reverse("verify"), **headers)

    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_verify_error(client):
    headers = {"Content-Type": "application/json", "HTTP_JWT": "someTokenThatISNotOKAY"}
    resp = client.post(reverse("verify"), **headers)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_register_endpoint(client):
    data = {"username": "james", "password": "Raccon"}
    resp = client.post(reverse("register"), data=data, format="json")

    assert resp.data["username"] == "james"
    assert resp.data["role"] == 0
    assert "JWT" in resp.data.keys()


@pytest.mark.django_db
def test_register_user_already_exists(client, generate_user):
    data = {"username": "mic", "password": "Raccon"}
    resp = client.post(reverse("register"), data=data, format="json")

    expected_data = "User With This Username Already Exists."
    assert resp.status_code == 400
    assert resp.data["username"][0].title() == expected_data


@pytest.mark.django_db
def test_change_role_endpoint(client, get_verified_user, generate_user):
    role = ApiUser.objects.filter(username="mic").first().role
    data = {"username": "mic"}
    headers = {"HTTP_JWT": get_verified_user["JWT"]}
    resp = client.post(reverse("change_role"), data=data, **headers)
    fliped_role = ApiUser.objects.filter(username="mic").first().role

    assert role != fliped_role


@pytest.mark.django_db
def test_comments_endpoint(fake_worker, client, get_verified_user):
    headers = {"HTTP_JWT": get_verified_user["JWT"]}
    resp = client.get(reverse("user_comments"), **headers)

    username = get_verified_user["username"]
    data = resp.data[username][0]

    test_keys = set(["id", "review", "text", "created_at", "updated_at", "show"])
    assert test_keys.issubset(data.keys())


@pytest.mark.django_db
def test_reviews_endpoint(fake_worker, client, get_verified_user):
    headers = {"HTTP_JWT": get_verified_user["JWT"]}
    resp = client.get(reverse("user_reviews"), **headers)

    username = get_verified_user["username"]
    data = resp.data[username][0]

    test_keys = set(["id", "text", "created_at", "updated_at", "show"])
    assert test_keys.issubset(set(data.keys()))


@pytest.mark.django_db
def test_favorites_endpoint(fake_worker, client, get_verified_user):
    headers = {"HTTP_JWT": get_verified_user["JWT"]}
    resp = client.get(reverse("user_favorites"), **headers)

    username = get_verified_user["username"]
    data = resp.data[username][0]

    test_keys = set(["id", "username", "created_at", "updated_at", "show"])
    assert test_keys.issubset(set(data.keys()))


@pytest.mark.django_db
def test_queue_request_when_token_unauthenticated(fake_worker, client):
    headers = {"HTTP_JWT": "someTokenThatISNotOKAY"}
    resp = client.get(reverse("user_favorites"), **headers)

    assert resp.status_code == 403
