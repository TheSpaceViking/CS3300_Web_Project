from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Avg

class Platform(models.Model):
    platform_choices = (
        #currently existing platforms as per the internet.
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
    cover_image = models.ImageField(upload_to='game_covers/', null=True, blank=True)
    
    def __str__(self):
        return self.title

    def calculate_overall_average_rating(self):
        reviews = Review.objects.filter(game=self, review_ratings__isnull=False)
        if reviews.exists():
            overall_ratings = [review.review_ratings.overall_rating for review in reviews]
            average_rating = sum(overall_ratings) / len(overall_ratings)
            self.overall_rating = round(average_rating * 2) / 2
        else:
            self.overall_rating = None




class Rating(models.Model):
    review = models.OneToOneField(
        'Review',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='review_ratings'
    )
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1)
    gameplay_rating = models.DecimalField(max_digits=2, decimal_places=1)
    graphics_rating = models.DecimalField(max_digits=2, decimal_places=1)
    sound_rating = models.DecimalField(max_digits=2, decimal_places=1)
    story_rating = models.DecimalField(max_digits=2, decimal_places=1)

    def update_review_on_rating_save(self):
        if self.review:  # Check if the rating is related to a review
            # Calculate the average overall rating for all ratings related to the same review
            average_rating = Rating.objects.filter(review=self.review).aggregate(Avg('overall_rating'))['overall_rating__avg']

            if average_rating is not None:
                self.review.overall_rating = round(average_rating * 2) / 2
                self.review.save()
    
    
    def __str__(self):
        return str(self.overall_rating)
    

class Review(models.Model):
    title = models.CharField(max_length=200, default="")
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField(max_length=1000)
    overall_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.overall_rating:
            if hasattr(self, 'review_ratings') and self.review_ratings.count() > 0:
                # Calculate the average overall rating from related ratings
                average_rating = self.review_ratings.aggregate(Avg('overall_rating'))['overall_rating__avg']
                if average_rating is not None:
                    self.overall_rating = round(average_rating * 2) / 2
        super().save(*args, **kwargs)

#this is where the ratings average out to give the review an overall rating
@receiver(post_save, sender=Rating)
def update_review_on_rating_save(sender, instance, **kwargs):
    if instance.review:
        # Calculate the average overall rating for all ratings related to the same review
        average_rating = Rating.objects.filter(review=instance.review).aggregate(Avg('overall_rating'))['overall_rating__avg']

        if average_rating is not None:
            instance.review.overall_rating = round(average_rating * 2) / 2
            instance.review.save()

#the review checks to see if there is an overall rating, and if not, it sets it.            
@receiver(pre_save, sender=Review)
def update_review_overall_rating(sender, instance, **kwargs):
    if not instance.overall_rating and hasattr(instance, 'review_ratings') and instance.review_ratings.count() > 0:
        # Calculate the average overall rating from related ratings
        average_rating = instance.review_ratings.aggregate(Avg('overall_rating'))['overall_rating__avg']
        if average_rating is not None:
            instance.overall_rating = round(average_rating * 2) / 2
        # Update the overall rating of the associated game
        if instance.game:
            instance.game.calculate_overall_average_rating()
            instance.game.save()