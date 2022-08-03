import pytest
from gateway.views import (
    get_username,
    get_relative_url,
    get_desired_api,
    validate_token,
)


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNyIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.3HYBCcw4LCQ9qVoyl-tlmxpNtihK4mG843LEiMzOlHE"


@pytest.mark.django_db
def test_get_desired_service(create_test_data):
    service = "sth"
    api = get_desired_api("sth")


def test_get_username():
    test_token = TOKEN
    expected_username = "John Doe"

    actual_username = get_username(test_token)

    assert expected_username == actual_username


def test_relative_url():
    url = "http:www.google.com/api/mic/jaguar"
    actual_relative_path = get_relative_url(url)
    expected_relative_path = "mic/jaguar"

    assert actual_relative_path == expected_relative_path


@pytest.mark.django_db
def test_validate_token(fake_validation, create_test_data):
    test_token = TOKEN

    is_token = validate_token(test_token)

    assert is_token == True
