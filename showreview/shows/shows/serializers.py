from rest_framework import serializers
from .models import Show, Comment, Review, Favorites, Character, Season, Episode


class EpisodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Episode
        fields = '__all__'
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0

class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorites
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


