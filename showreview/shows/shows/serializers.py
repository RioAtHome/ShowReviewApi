from rest_framework import serializers
from .models import Show, Comment, Review, Favorites, Character, Season, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source="Show.show")
    season_name = serializers.CharField(source="Season.name")

    class Meta:
        model = Season
        fields = '__all__'
        extra_fields = ['show_name', 'season_name']
        depth = 1


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'
        


class ShowSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = Show
        fields = '__all__'
        extra_fields = ['season']


class CommentSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source="Show.show")

    class Meta:
        model = Comment
        fields = '__all__'
        extra_fields = ['show_name']


class ReviewSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source="Show.show")

    class Meta:
        model = Review
        fields = '__all__'
        extra_fields = ['show_name']


class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorites
        fields = '__all__'


class FullNameField(serializers.Field):
    def to_representation(self, value):
        return value.get_full_name()

    def to_internal_value(self, full_name):
        first_name, middle_name, last_name = full_name.split(" ")
        return {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
        }


class CharacterSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source="Show.show")

    class Meta:
        model = Character
        fields = [
            "show_name",
            "first_name",
            "age",
            "gender",
            "status",
            "created_at",
            "updated_at",
        ]
