from django.urls import path, include
from .views import verify, register, change_role, view_comments, view_reviews, view_favorites, view_homepage

urlpatterns = [
    path('verify/', verify),
    path('register/', register),
    path('change-role/', change_role),
    path('comments/', view_comments),
    path('reviews/', view_comments),
    path('favorites/', view_favorites),
    path('favorites/', view_homepage)

]