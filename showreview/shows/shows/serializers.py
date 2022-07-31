from rest_framework import serializers
from .models import Show, Comment, Review, Favorites, Character, Season, Episode


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


class ShowSerializer(serializers.ModelSerializer):
    seasons = serializers.StringRelatedField(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    characters = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Show
        fields = "__all__"
        extra_fields = ["seasons", "reviews", "characters"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        depth = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context
        if method == "POST":
            self.Meta.depth = 0


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = "__all__"


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["username"]


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ["username"]


class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        exclude = ["ussername"]
