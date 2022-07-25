import jwt, datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django.conf import settings
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

def get_payload(request):
    try:
        token = request.META['HTTP_JWT']
    except KeyError:
        raise AuthenticationFailed("Token is needed")

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        raise e

    return payload


@api_view(["GET"])
def shows_view(request):
    queryset = Show.objects.all()[:3]
    serializer = ShowSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def show_view(request, *args, **kwargs):
    show_name = kwargs['show_name'].lower()
    if request.method == "GET":
        queryset = Show.objects.all().filter(show=show_name).first()
        if queryset is None:
            raise NotFound()
        serializer = ShowSerializer(queryset)
        
        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)
        if payload['rol'] == "A":
            serializer = ShowSerializer(date=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")


@api_view(["GET", "POST"])
def season_view(request, *args, **kwargs):
    season_id = kwargs['season_id']
    if request.method == "GET":
        queryset = Season.objects.all().filter(id=season_id).first()
        if queryset is None:
            raise NotFound()
        serializer = SeasonSerializer(queryset)

        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)
        if payload['rol'] == "A":
            serializer = SeasonSerializer(date=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")


@api_view(["GET", "POST"])
def episode_view(request, *args, **kwargs):
    epi_id = kwargs['epi_id']
    if request.method == "GET":
        queryset = Episode.objects.all().filter(id=epi_id).first()
        if queryset is None:
            raise NotFound()
        serializer = EpisodeSerializer(queryset)

        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)
        if payload['rol'] == "A":
            serializer = EpisodeSerializer(date=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")

@api_view(["GET", "POST"])
def character_view(request, *args, **kwargs):
    char_name = kwargs['char_name']
    if request.method == "GET":
        queryset = Character.objects.all().filter(first_name=char_name).first()
        if queryset is None:
            raise NotFound()
        serializer = CharacterSerializer(queryset)

        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)
        if payload['rol'] == "A":
            serializer = CharacterSerializer(date=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")



@api_view(["GET", "POST"])
def review_view(request, *args, **kwargs):
    if request.method == "GET":
        pass

    elif request.method == "POST":
        payload = get_payload(request)
        pass


@api_view(["GET", "POST"])
def comment_view(request):
    if request.method == "GET":
        pass

    elif request.method == "POST":
        pass


@api_view(["POST"])
def favorite(request, *args, **kwargs):
    pass
