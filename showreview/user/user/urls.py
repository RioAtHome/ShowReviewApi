from django.urls import path, include
from .views import (
    verify,
    register,
    change_role,
    view_comments,
    view_reviews,
    view_favorites,
)

urlpatterns = [
    path("verify/", verify, name="verify"),
    path("register/", register, name="register"),
    path("change-role/", change_role, name="change_role"),
    path("comments/", view_comments, name="user_comments"),
    path("reviews/", view_reviews, name="user_reviews"),
    path("favorites/", view_favorites, name="user_favorites"),
]
