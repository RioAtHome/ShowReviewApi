from django.db import models
from django.core.validators import MinValueValidator

class Show(models.Model):
    show = models.CharField(max_length=200, primary_key=True)
    network = models.CharField(max_length=200)
    air_date = models.DateTimeField()
    end_date = models.DateTimeField()
    num_of_favorites = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    username = models.CharField(max_length=200)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Review(models.Model):
    username = models.CharField(max_length=200)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Favorites(models.Model):
    username = models.CharField(max_length=200)
    show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Character(models.Model):
    STATUS = (('D', 'MALE'), ('A', 'Female'), ('U', 'Unknown'))
    GENDER = (('M', 'MALE'), ('F', 'Female'))

    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    status = models.CharField(max_length=1, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    number_of_episodes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    number_of_episode = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    release_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
