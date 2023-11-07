from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Game, Platform, Genre
from .forms import ReviewForm, GameForm, GenreForm, PublisherForm, RatingForm

# Create your views here.
def index(request):
    games = Game.objects.all()
    return render( request, 'gameReview_app/index.html', {'games': games} )

def game_list(request):
    games = Game.objects.all()
    return render(request, 'gameReview_app/game_list.html', {'games': games})

def game_detail(request, game_id):
    # Retrieve the game instance
    game = Game.objects.get(pk=game_id)
    
    if request.method == 'POST':
        # If a POST request, process the form
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Save the form with the current game instance
            review = review_form.save(commit=False)
            review.game = game  # Set the game instance
            review.save()
            return redirect('game_detail', game_id=game_id)
    else:
        # If a GET request, display the form
        review_form = ReviewForm()

    return render(request, 'gameReview_app/game_detail.html', {'game': game, 'review_form': review_form})

def platform_list(request):
    platforms = Platform.objects.all()
    return render(request, 'gameReview_app/platform_list.html', {'platforms': platforms})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'gameReview_app/genre_list.html', {'genres': genres})

def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            # Optionally, you can redirect to the game's detail page or another appropriate page.
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm()
    
    return render(request, 'gameReview_app/game_form.html', {'form': form})

def create_review(request, game_id):
    game = Game.objects.get(pk=game_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        rating_form = RatingForm(request.POST)

        if review_form.is_valid() and rating_form.is_valid():
            review = review_form.save(commit=False)
            review.game = game
            review.save()  # Save the Review instance first

            rating = rating_form.save(commit=False)
            rating.game = game
            rating.review = review
            rating.save()  # Save the Rating instance after the Review instance

            # Redirect to the game details page or another view
            return redirect('game_detail', game_id=game_id)
    else:
        review_form = ReviewForm()
        rating_form = RatingForm()

    return render(request, 'gameReview_app/review_form.html', {
        'game': game,
        'review_form': review_form,
        'rating_form': rating_form,
    })
