from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import admin

class Platform(models.Model):
    platform_choices = (
        ('PS5', 'PlayStation 5'),
        ('XBOX_SERIES_X', 'Xbox Series X'),
        ('SWITCH', 'Nintendo Switch'),
        ('PC', 'PC'),
        ('PS4', 'PlayStation 4'),
        ('XBOX_ONE', 'Xbox One'),
        ('PS3', 'PlayStation 3'),
        ('XBOX_360', 'Xbox 360'),
        ('WII_U', 'Wii U'),
        ('WII', 'Wii'),
        ('PS2', 'PlayStation 2'),
        ('GAMECUBE', 'GameCube'),
        ('N64', 'Nintendo 64'),
        ('PS1', 'PlayStation 1'),
        ('SEGA_GENESIS', 'Sega Genesis'),
        ('SNES', 'Super Nintendo Entertainment System'),
        ('NES', 'Nintendo Entertainment System'),
        ('ATARI_2600', 'Atari 2600'),
        ('GAME_BOY', 'Nintendo Game Boy'),
        ('SEGA_MASTER_SYSTEM', 'Sega Master System'),
        ('XBOX', 'XBOX'),
        ('SEGA_SATURN', 'Sega Saturn'),
        ('SEGA_DREAMCAST', 'Sega Dreamcast'),
        ('SEGA_GAME_GEAR', 'Sega Game Gear'),
        ('NDS', 'Nintendo DS'),
        ('GBC', 'Nintendo Game Boy Color'),
        ('NVB', 'Nintendo Virtual Boy'),
        # Add more platforms here
    )
    platform_choices = sorted(platform_choices, key=lambda x: x[1])
    name = models.CharField(max_length=50, choices=platform_choices)

    def __str__(self):
        return self.get_name_display()


class Genre(models.Model):
    genre_choices = (
        ('ACTION', 'Action'),
        ('ADVENTURE', 'Adventure'),
        ('RPG', 'Role-Playing Game'),
        ('STRATEGY', 'Strategy'),
        ('SPORTS', 'Sports'),
        ('SIMULATION', 'Simulation'),
        ('PUZZLE', 'Puzzle'),
        ('HORROR', 'Horror'),
        ('SHOOTER', 'Shooter'),
        ('PLATFORMER', 'Platformer'),
        ('RACING', 'Racing'),
        ('FIGHTING', 'Fighting'),
        ('MOBA', 'MOBA'),
        ('SURVIVAL', 'Survival'),
        ('SANDBOX', 'Sandbox'),
        ('STEALTH', 'Stealth'),
        ('MUSIC', 'Music'),
        ('EDUCATIONAL', 'Educational'),
        ('OPEN_WORLD', 'Open World'),
        ('OTHER', 'Other'),
    )
    genre_choices = sorted(genre_choices, key=lambda x: x[1])
    game_genre = models.CharField(max_length=50, choices=genre_choices)
    
    def __str__(self):
        return self.get_game_genre_display()


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    contact = models.CharField(max_length=200)

from django.db import models

# ... other model definitions ...

class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    release_year = models.DateField()
    platforms = models.ManyToManyField(Platform)
    overall_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def calculate_overall_average_rating(self):
        reviews = self.reviews.all()  # Access reviews using the correct related name
        if reviews:
            overall_ratings = [review.overall_rating for review in reviews]
            average_rating = sum(overall_ratings) / len(overall_ratings)
            self.overall_rating = round(average_rating * 2) / 2
        else:
            self.overall_rating = None


class Rating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    overall_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    gameplay_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    graphics_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    sound_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    story_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    
    def __str__(self):
        return self.get_overall_rating_display()

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField(max_length=1000)
    overall_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.rating_set.count() > 0:
            subratings = [rating.overall_rating for rating in self.rating_set.all()]
            average_rating = sum(subratings) / len(subratings)
            self.overall_rating = round(average_rating * 2) / 2
        super().save(*args, **kwargs)
