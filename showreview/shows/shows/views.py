import jwt, datetime
from jwt.exceptions import DecodeError
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


SERAILIZER_MAP = {
    'show': [ShowSerializer, Show],
    'comment':[CommentSerializer, Comment],
    'review':[ReviewSerializer, Review],
    'favorite':[FavoritesSerializer, Favorites],
    'character':[CharacterSerializer, Character],
    'season':[SeasonSerializer, Season],
    'episode':[EpisodeSerializer, Episode]
}

def get_payload(request):
    try:
        token = request.META['HTTP_JWT']
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
        if model in ('review', 'comment'):
            queryset = model.objects.filter(**filter_)[:3]
        else:
            queryset = model.objects.filter(**filter_).first()
        if queryset is None:
            raise NotFound()
        s = serializer(queryset, context=method)

        return Response(s.data)

    elif method == "POST":
        payload = get_payload(request)
        data = request.data

        if _model in ('review', 'comment'):
            data['username'] = payload['usr']

        data.update(filter_)
        print(data)
        if auth:
            if payload['rol'] != 1:
                raise AuthenticationFailed("User is not Authorized to edit/create data.")
        queryset = model.objects.filter(**filter_).first()
        
        if queryset is not None:
            return Response(f"Data already exists", status=404)


        s = serializer(data=data, context=method)
        s.is_valid(raise_exception=True)

        if _model == 'episode':
            season = Season.objects.filter(season_num=data['season'])
            number_of_episodes = season[0].number_of_episodes + 1

            season.update(number_of_episodes=number_of_episodes)
        
        s.save()



        context = {
        "message": "Data has been added successfully",
        "data": s.data
        }

        return Response(context, status=201)


@api_view(["GET"])
def shows_view(request):
    queryset = Show.objects.all()[:3]
    serializer = ShowSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["GET", "POST"])
def show_view(request, *args, **kwargs):
    filter_ = {'show':kwargs['show_name']}
    return handle_request(request, 'show', filter_, True)

@api_view(["GET", "POST"])
def season_view(request, *args, **kwargs):
    filter_ = {'season_num':kwargs['season_num'], 'show':kwargs['show_name']}
    
    return handle_request(request, 'season', filter_, True)

@api_view(["GET", "POST"])
def episode_view(request, *args, **kwargs):
    filter_ = {'epi_num': kwargs['epi_num'], 'season': kwargs['season_num'], 'show':kwargs['show_name']}
    
    return handle_request(request, 'episode', filter_, True)

# remove the whole last/first name
@api_view(["GET", "POST"])
def character_view(request, *args, **kwargs):
    filter_ = {'name':kwargs['char_name'], 'show':kwargs['show_name']}

    return handle_request(request, 'character', filter_, True)

@api_view(["GET", "POST"])
def review_view(request, *args, **kwargs):
    filter_ = {'show':kwargs['show_name']}
    return handle_request(request, 'review', filter_)

@api_view(["GET", "POST"])
def comment_view(request, *args, **kwargs):
    filter_ = {'review': kwargs['review_id'], 'show': kwargs['show_name']}
    
    return handle_request(request, 'comment', filter_)

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
