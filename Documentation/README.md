# CS3300_Web_Project
Game ranking and review webpage for CS3300 final project.
See technical document for setup and code functionality

for any migration issues and you need to start over on the DB but have genres and platforms refresh their objects, place
this code into the migration file created by makemigrations BEFORE migrating


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