import jwt, datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import Show, Comment, Review, Favorites, Character, Season, Episode
from .serializers import ShowSerializer, CommentSerializer, ReviewSerializer, FavoritesSerializer, CharacterSerializer, SeasonSerializer, EpisodeSerializer

@api_view(['GET'])
def shows_view(request):
	pass

@api_view(['GET', 'POST', 'UPDATE'])
def show_view(request):
	pass

@api_view(['GET', 'POST', 'UPDATE'])
def season_view(request):
	pass

@api_view(['GET', 'POST', 'UPDATE'])
def comment_view(request):
	pass

@api_view(['GET', 'POST', 'UPDATE'])
def episode_view(request):
	pass

@api_view(['GET', 'POST', 'UPDATE'])
def review_view(request):
	pass

@api_view(['GET', 'POST', 'UPDATE'])
def character_view(request):
	pass

@api_view(['POST'])
def favorite(request):
	pass