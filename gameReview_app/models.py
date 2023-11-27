from django.db import models
from django.http import HttpRequest
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Avg
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

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

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize email to lowercase
        user = self.model(email=email, first_name=first_name, last_name=last_name, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        # Create a superuser with the provided information
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user_name = f'admin{self.model.objects.count() + 1}'  # Set user_name as "admin" + the user's id
        return self.create_user(email, first_name, last_name, user_name, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff status', default=False)
    # Add a field to represent selected genres
    favorite_genres = models.ManyToManyField(Genre, blank=True)
    # Add related_name arguments to avoid conflicts
    groups = models.ManyToManyField(Group, verbose_name='Groups', blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name='User Permissions', blank=True, related_name='custom_user_set')

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.user_name

class Platform(models.Model):
    platform_choices = (
        # Currently existing platforms as per the internet.
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

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    contact = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


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
    cover_image = models.ImageField(upload_to='game_covers/', null=True, blank=True) # Saves the uploaded image to media/game_covers
    
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
        'gameReview_app.Review',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='review_ratings'
    )
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    gameplay_rating = models.DecimalField(max_digits=2, decimal_places=1)
    graphics_rating = models.DecimalField(max_digits=2, decimal_places=1)
    sound_rating = models.DecimalField(max_digits=2, decimal_places=1)
    story_rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.review} rating"

    def save(self, *args, **kwargs):
        if self.review:
            # Calculate the overall rating as an average of individual ratings
            gameplay_rating = Decimal(str(self.gameplay_rating))
            graphics_rating = Decimal(str(self.graphics_rating))
            sound_rating = Decimal(str(self.sound_rating))
            story_rating = Decimal(str(self.story_rating))
            
            overall_rating = (gameplay_rating + graphics_rating +
                              sound_rating + story_rating) / Decimal(4)

            # Round to one decimal place, e.g., 3.725 -> 3.7
            self.overall_rating = overall_rating.quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)

            # Update the associated review's overall_rating
            self.review.overall_rating = self.overall_rating
            self.review.save()

        super().save(*args, **kwargs)
    
    
class Review(models.Model):
    title = models.CharField(max_length=200, default="")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=1000)
    overall_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)  # Add this line

    def save(self, *args, **kwargs):
        # Get the currently logged-in user from the request object
        user = self._get_current_user()

        if user:
            self.user = user

        super().save(*args, **kwargs)

        if self.game:
            self.game.calculate_overall_average_rating()
            self.game.save()

    def _get_current_user(self):
        # This function tries to get the currently logged-in user from the request object
        # You should pass the request object when saving a review
        if hasattr(HttpRequest, 'user') and self._request.user.is_authenticated:
            return self._request.user
        return None
    
    def __str__(self):
        return f"{self.title} - {self.game}"

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