from rest_framework import serializers
from .models import Show, Comment, Review, Favorites, Character, Season, Episode


class ShowSerializer(serializers.ModelSerializer):
	pass

class CommentSerializer(serializers.ModelSerializer):
	pass

class ReviewSerializer(serializers.ModelSerializer):
	pass

class FavoritesSerializer(serializers.ModelSerializer):
	pass

class CharacterSerializer(serializers.ModelSerializer):
	pass

class SeasonSerializer(serializers.ModelSerializer):
	pass

class EpisodeSerializer(serializers.ModelSerializer):
	pass

