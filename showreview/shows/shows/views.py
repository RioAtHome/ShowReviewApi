import jwt, datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
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


# in total, change gets to get more information about each topin
# Show views characters, seasons, episodes reviews.

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
        if payload['rol'] == 1:
            serializer = ShowSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")

        return Response(f"Show:{serializer.data['show']} with id:{serializer.data['id']} has been added")


@api_view(["GET", "POST"])
def season_view(request, *args, **kwargs):
    season_num = kwargs['season_num']
    show_name = kwargs['show_name']

    if request.method == "GET":
        queryset = Season.objects.filter(show__show=show_name, season_num=season_num).first()
        if queryset is None:
            raise NotFound()
        serializer = SeasonSerializer(queryset)

        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)

        if payload['rol'] == 1:
            season = Season.objects.filter(show__show=show_name, season_num=season_num).first()
            
            if season is not None:
                return Response(f"Season already exists", status=404)
            
            data = request.data
            data['season_num'] = season_num
            data['show_name'] = show_name
            serializer = SeasonSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")

        return Response(f"Season:{serializer.data['season_num']} has been added")

@api_view(["GET", "POST"])
def episode_view(request, *args, **kwargs):
    epi_num = kwargs['epi_num']
    season_num = kwargs['season_num']
    show_name = kwargs['show_name']
    if request.method == "GET":
        queryset = Episode.objects.filter(show__show=show_name, season__season_num=season_num, epi_num=epi_num).first()
        if queryset is None:
            raise NotFound()
        serializer = EpisodeSerializer(queryset)

        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)
        if payload['rol'] == 1:
            episode = Episode.objects.filter(show__show=show_name, season__season_num=season_num, epi_num=epi_num).first()
            if episode is not None:
                return Response(f"Episode already exists", status=404)
            
            data = request.data

            data['epi_num'] = epi_num
            data['season_num'] = season_num
            data['show_name'] = show_name


            serializer = EpisodeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed("User is not Authorized to edit/create data.")


# remove the whole last/first name
@api_view(["GET", "POST"])
def character_view(request, *args, **kwargs):
    char_name = kwargs['char_name']
    show_name = kwargs['show_name']
    if request.method == "GET":
        queryset = Character.objects.filter(show__show=show_name, first_name=char_name).first()
        if queryset is None:
            raise NotFound()
        serializer = CharacterSerializer(queryset)

        return Response(serializer.data)

    elif request.method == "POST":
        payload = get_payload(request)
        if payload['rol'] == 1:
            char_name = kwargs['char_name']
            show_name = kwargs['show_name']
            data = request.data
            data['show_name'] = show_name
            data['first_name'] = char_name
            serializer = CharacterSerializer(data=data)
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
    payload = get_payload(request)
    user = payload['usr']
    show_name = kwargs["show_name"]
    show = Show.objects.filter(show=show_name)
    serializer = FavoritesSerializer(data={'username': user, 'show':show_name})
    serializer.is_valid(raise_exception=True)
    
    num_of_favorites = show[0].num_of_favorites + 1
    show.update(num_of_favorites=num_of_favorites)

    serializer.save()

    return Response(f"Show:{show_name} has been added to user {user} favorites")


