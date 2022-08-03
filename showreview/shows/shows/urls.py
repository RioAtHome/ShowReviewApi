from django.urls import path, include
from .views import (
    shows_view,
    show_view,
    season_view,
    comment_view,
    episode_view,
    review_view,
    character_view,
    favorite,
)

urlpatterns = [
    path("", shows_view, name='get_all_shows'),
    path("<str:show_name>/", show_view, name='show'),
    path("<str:show_name>/<int:season_num>/", season_view, name='season'),
    path("<str:show_name>/favorites/", favorite, name='favorite'),
    path("<str:show_name>/<int:season_num>/<int:epi_num>/", episode_view, name='episode'),
    path("<str:show_name>/character/<str:char_name>/", character_view, name='character'),
    path("<str:show_name>/reviews/", review_view, name='review'),
    path("<str:show_name>/reviews/<str:review_id>/comments/", comment_view, name='comment'),
]
