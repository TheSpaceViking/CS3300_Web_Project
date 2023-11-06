# Generated by Django 4.2.6 on 2023-11-06 05:22
from django.db import migrations
from gameReview_app.models import Platform, Genre

def create_initial_platforms_and_genres(apps, schema_editor):
    # Access the models using the historical version of the app registry
    Platform = apps.get_model('gameReview_app', 'Platform')
    Genre = apps.get_model('gameReview_app', 'Genre')

    # Create instances for platforms
    platforms = [
        'PS5', 'XBOX_SERIES_X', 'SWITCH', 'PC', 'PS4','XBOX_ONE', 'PS3', 'XBOX_360', 'WII_U', 'WII',
        'PS2', 'GAMECUBE', 'N64', 'PS1', 'SEGA_GENESIS', 'SNES', 'NES', 'ATARI_2600', 'GAME_BOY', 'SEGA_MASTER_SYSTEM',
        'XBOX', 'SEGA_SATURN', 'SEGA_DREAMCAST', 'SEGA_GAME_GEAR', 'NDS', 'GBC', 'NVB', 
    ] # Add all platform choices
    for platform in platforms:
        Platform.objects.create(name=platform)

    # Create instances for genres
    genres = [
        'ACTION', 'ADVENTURE', 'RPG', 'STRATEGY', 'SPORTS', 'SIMULATION', 'PUZZLE', 'HORROR', 'SHOOTER', 'PLATFORMER', 
        'RACING', 'FIGHTING', 'MOBA', 'SURVIVAL', 'SANDBOX', 'STEALTH', 'MUSIC', 'EDUCATIONAL', 'OPEN_WORLD', 'OTHER',
    ]  # Add all genre choices
    for genre in genres:
        Genre.objects.create(game_genre=genre)

class Migration(migrations.Migration):
    dependencies = [
        ('your_app_name', '000x_previous_migration'),
    ]

    operations = [
        migrations.RunPython(create_initial_platforms_and_genres),
    ]


class Migration(migrations.Migration):

    dependencies = [
        ('gameReview_app', '0005_auto_20231105_2219'),
    ]

    operations = [
        migrations.RunPython(create_initial_platforms_and_genres),
    ]