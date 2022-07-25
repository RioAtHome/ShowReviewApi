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
    path("", shows_view),
    path("<str:show_name>/", show_view),
    path("<str:show_name>/<int:season_num>/", season_view),
    path("<str:show_name>/favorites", favorite),
    path("<str:show_name>/<int:season_num>/<int:epi_num>/", episode_view),
    path("<str:show_name>/character/<str:char_name>", character_view),
    path("<str:show_name>/reviews", review_view),
    path("<str:show_name>/<str:review_id>/comments", comment_view),
]
