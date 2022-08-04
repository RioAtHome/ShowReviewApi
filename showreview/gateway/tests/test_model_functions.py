import pytest
from django.test import RequestFactory
from gateway.models import Api


@pytest.mark.django_db
def test_api_gets_created():
    new_data = Api(1, "sth", "https://www.testtheurl.com/")
    new_data.save()
    data = Api.objects.filter(name="sth").first()

    assert new_data is not None


@pytest.mark.django_db
@pytest.mark.parametrize(
    "request_method",
    [
        RequestFactory().get,
        RequestFactory().post,
        RequestFactory().put,
        RequestFactory().delete,
    ],
)
def test_handle_request(disable_network_calls, request_method):
    api = Api(1, "sth", "https://www.testtheurl.com/")
    url = "http://apigateway.com/api/service/something"

    headers = {"content_type": "application/json", "jwt": "token"}
    data = {"username": "sth", "password": "sthelse"}

    request = request_method(url, **headers)
    request.data = data

    resp = api.handle_request(request, "service/something", "token")

    assert "jwt" in resp.headers

    assert "username", "password" in resp.data
