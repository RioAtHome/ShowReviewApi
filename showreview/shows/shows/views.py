import jwt
from jwt.exceptions import DecodeError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound

from .models import Show, Comment, Review, Favorites, Character, Season, Episode
from .serializers import (
    ShowSerializer,
    CommentSerializer,
    ReviewSerializer,
    FavoritesSerializer,
    CharacterSerializer,
    SeasonSerializer,
    EpisodeSerializer,
)


SERAILIZER_MAP = {
    "show": [ShowSerializer, Show],
    "comment": [CommentSerializer, Comment],
    "review": [ReviewSerializer, Review],
    "favorite": [FavoritesSerializer, Favorites],
    "character": [CharacterSerializer, Character],
    "season": [SeasonSerializer, Season],
    "episode": [EpisodeSerializer, Episode],
}


def get_payload(request):
    try:
        token = request.META["HTTP_JWT"]
    except KeyError:
        raise AuthenticationFailed("Token is needed")

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except DecodeError:
        raise AuthenticationFailed("Token is invalid")

    return payload


def handle_request(request, model, filter_, auth=False):
    _model = model
    serializer = SERAILIZER_MAP[model][0]
    model = SERAILIZER_MAP[model][1]
    method = request.method
    if method == "GET":
        if _model in ("review", "comment"):
            queryset = model.objects.filter(**filter_)[:3]
            s = serializer(queryset, context=method, many=True)
        else:
            queryset = model.objects.filter(**filter_).first()
            s = serializer(queryset, context=method)
        if queryset is None:
            raise NotFound()

        context = {_model: s.data}

        return Response(context)

    elif method == "POST":
        payload = get_payload(request)
        data = request.data

        if _model in ("review", "comment", "favorite"):
            data["username"] = payload["usr"]

        data.update(filter_)

        if auth:
            if payload["rol"] != 1:
                raise AuthenticationFailed(
                    "User is not Authorized to edit/create data."
                )

        if _model in ("episode", "season"):
            queryset = model.objects.filter(**filter_).first()
            if queryset is not None:
                return Response(f"Data already exists", status=404)

        s = serializer(data=data, context=method)
        s.is_valid(raise_exception=True)
        s.save()

        context = {"message": "Data has been added successfully", "data": s.data}

        return Response(context, status=201)
    elif method == "PUT":
        queryset = model.objects.filter(**filter_).first()
        s = serializer(queryset, data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response({"message": "Data has been updated successfully"})
        

    elif method == "DELETE":
        model.objects.filter(**filter_).delete()
        return Response({"message": "Data has been deleted successfully"})

@api_view(["GET"])
def shows_view(request):
    queryset = Show.objects.all()[:3]
    serializer = ShowSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST", "DELETE", "PUT"])
def show_view(request, *args, **kwargs):
    filter_ = {"show": kwargs["show_name"]}
    return handle_request(request, "show", filter_, True)


@api_view(["GET", "POST", "DELETE", "PUT"])
def season_view(request, *args, **kwargs):
    filter_ = {"season_num": kwargs["season_num"], "show": kwargs["show_name"]}

    return handle_request(request, "season", filter_, True)


@api_view(["GET", "POST", "DELETE", "PUT"])
def episode_view(request, *args, **kwargs):
    filter_ = {
        "epi_num": kwargs["epi_num"],
        "season": kwargs["season_num"],
        "show": kwargs["show_name"],
    }

    return handle_request(request, "episode", filter_, True)


@api_view(["GET", "POST", "DELETE", "PUT"])
def character_view(request, *args, **kwargs):
    filter_ = {"name": kwargs["char_name"], "show": kwargs["show_name"]}

    return handle_request(request, "character", filter_, True)


@api_view(["GET", "POST", "DELETE", "PUT"])
def review_view(request, *args, **kwargs):
    filter_ = {"show": kwargs["show_name"]}
    return handle_request(request, "review", filter_)


@api_view(["GET", "POST", "DELETE", "PUT"])
def comment_view(request, *args, **kwargs):
    filter_ = {"review": kwargs["review_id"], "show": kwargs["show_name"]}

    return handle_request(request, "comment", filter_)


@api_view(["POST"])
def favorite(request, *args, **kwargs):
    filter_ = {"show": kwargs["show_name"]}

    return handle_request(request, "favorite", filter_)
