import jwt, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .serializers import ApiUserSerializer
from .models import ApiUser
from .requestqueue import RequestQueue

# Create your views here.


requestqueue = RequestQueue()


def verify_token(request):
    try:
        token = request.META["HTTP_JWT"]
    except KeyError:
        raise AuthenticationFailed("Token not provided")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        raise AuthenticationFailed("Unauthenticated!")
    return payload


def queue_request(request, model):
    payload = verify_token(request)
    requested_data = {
        "username": payload["usr"],
        "_model": model,
    }
    shows_response = requestqueue.call(requested_data)
    if not shows_response:
        username = requested_data["username"]
        _model = requested_data["_model"]
        return Response(f"{username} has no {_model}", status=201)

    shows_response = {requested_data["username"]: shows_response}
    return Response(shows_response, status=201)


@api_view(["POST"])
def register(request):
    serializer = ApiUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    payload = {
        "usr": serializer.data["username"],
        "rol": serializer.data["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    data = {"JWT": token}

    data.update(serializer.data)

    return Response(data)


@api_view(["POST"])
def verify(request):
    payload = verify_token(request)

    return Response(
        {"message": "A-Okay buddy!"}, headers={"JWT": request.META["HTTP_JWT"]}
    )


@api_view(["POST"])
def change_role(request):
    payload = verify_token(request)

    flip_user = request.data["username"]
    admin_user = payload["usr"]

    admin = ApiUser.objects.filter(username=admin_user).first()
    if admin.role == 1:
        pass
    else:
        raise AuthenticationFailed("User Not authorized")

    user = ApiUser.objects.filter(username=flip_user).first()

    if user is None:
        raise AuthenticationFailed("User Not Found")

    role = user.role
    role ^= 1

    changes = ApiUser.objects.filter(username=flip_user).update(role=role)

    return Response({"message": "Fliped user!"})


@api_view(["GET"])
def view_comments(request):
    return queue_request(request, "comments")


@api_view(["GET"])
def view_reviews(request):
    return queue_request(request, "reviews")


@api_view(["GET"])
def view_favorites(request):
    return queue_request(request, "favorites")
