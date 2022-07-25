from django.contrib import admin
from .models import Show, Comment, Review, Favorites, Character, Season, Episode

# Register your models here.
admin.site.register(Show)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Favorites)
admin.site.register(Character)
admin.site.register(Season)
admin.site.register(Episode)