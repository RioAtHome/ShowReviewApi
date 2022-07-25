from django.urls import path, include
from .views import show_view, season_view, comment_view, episode_view, review_view, character_view, favorite

urlpatterns = [
    path('', show_view),
    path('<str:show_name>/', show_view),
    path('<str:show_name>/<int:season_id>/', season_view),
    path('<str:show_name>/favorites', favorite),
    path('<str:show_name>/<int:season_id>/<int:epi_id>/', episode_view),
    path('<str:show_name>/<str:char_name>', character_view),
    path('<str:show_name>/reviews', review_view),
    path('<str:show_name>/<str:review_id>/comments', comment_view)
]