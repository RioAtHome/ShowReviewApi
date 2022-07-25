from rest_framework import serializers
from .models import Show, Comment, Review, Favorites, Character, Season, Episode


class EpisodeSerializer(serializers.ModelSerializer):
	show_name = serializers.CharField(source='Show.show')
	season_name = serializers.CharField(source='Season.name')
	
	class Meta:
		model = Season
		fields = ['show_name', 'title', 'season_name','number_of_episode', 'release_date', 'created_at', 'updated_at']
		

class SeasonSerializer(serializers.ModelSerializer):
	show_name = serializers.CharField(source='Show.show')
	episodes = EpisodeSerializer(many=True, read_only=True)
	
	class Meta:
		model = Season
		fields = ['show_name', 'name', 'number_of_episodes', 'episodes', 'created_at', 'updated_at']


class ShowSerializer(serializers.ModelSerializer):
	seasons = SeasonSerializer(many=True, read_only=True)

	class Meta:
		model = Show
		fields = ['show', 'network', 'air_date', 'end_date', 'seasons', 'num_of_favorites', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
	show_name = serializers.CharField(source='Show.show')
	
	class Meta:
		model = Comment
		fields = ['username', 'show_name', 'text', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
	show_name = serializers.CharField(source='Show.show')
	
	class Meta:
		model = Review
		fields = ['username', 'show_name', 'text', 'created_at', 'updated_at']
	
class FavoritesSerializer(serializers.ModelSerializer):
	show_id = serializers.CharField(source='Show.id')
	
	class Meta:
		model = Favorites
		fields = ['username', 'show_id', 'created_at']
		

class FullNameField(serializers.Field):
	def to_representation(self, value):
		return value.get_full_name()

	def to_internal_value(self, full_name):
		first_name, middle_name, last_name = full_name.split(' ')
		return {'first_name': first_name, 'middle_name':middle_name, 'last_name':last_name}

class CharacterSerializer(serializers.ModelSerializer):
	show_name = serializers.CharField(source='Show.show')

	class Meta:
		model = Character
		fields = ['show_name', 'first_name', 'age', 'gender', 'status', 'created_at', 'updated_at']
		
