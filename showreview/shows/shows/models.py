from django.db import models
from django.core.validators import MinValueValidator


class Show(models.Model):
    class Meta:
        ordering = ['num_of_favorites']

    show = models.CharField(max_length=200, primary_key=True)
    network = models.CharField(max_length=200)
    air_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    num_of_favorites = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.show = self.show.lower().replace(' ', '-')
        self.network = self.network.lower()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.show


class Review(models.Model):
    username = models.CharField(max_length=200)
    show = models.ForeignKey(Show, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    username = models.CharField(max_length=200)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)



class Favorites(models.Model):
    username = models.CharField(max_length=200)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        show = Show.objects.filter(show=self.show.show)
        num_of_favorites = show[0].num_of_favorites + 1
        show.update(num_of_favorites=num_of_favorites)

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.show_id.id)


class Character(models.Model):
    STATUS = (("D", "Dead"), ("A", "Alive"), ("U", "Unknown"))
    GENDER = (("M", "MALE"), ("F", "Female"))

    show = models.ForeignKey(Show, related_name='characters',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    status = models.CharField(max_length=1, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Season(models.Model):
    show = models.ForeignKey(Show, related_name='seasons', on_delete=models.CASCADE)
    season_num = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    number_of_episodes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.season_num)


class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    epi_num = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        season = Season.objects.filter(season_num=self.season.season_num)
        number_of_episodes = season[0].number_of_episodes + 1
        season.update(number_of_episodes=number_of_episodes)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
