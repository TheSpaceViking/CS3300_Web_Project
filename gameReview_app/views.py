from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from .models import Game, Platform, Genre, User, Publisher
from .forms import ReviewForm, GameForm, UserRegistrationForm, PublisherForm, RatingForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_genres = request.user.favorite_genres.all()
        # Use Q objects and distinct to ensure unique games
        games = Game.objects.filter(Q(genre__in=user_genres) | Q(genre__isnull=True)).distinct()
    else:
        games = Game.objects.all()

    return render(request, 'gameReview_app/index.html', {'games': games})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def user_profile(request):
    # Your user profile logic here
    return render(request, 'index.html')

def redirect_to_index(request):
    return redirect('index')

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
    publishers = Publisher.objects.all()
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            # Optionally, you can redirect to the game's detail page or another appropriate page.
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm()
    
    return render(request, 'gameReview_app/game_form.html', {'form': form, 'publishers': publishers})

from django.contrib.auth.decorators import login_required

# ...

@login_required
def create_review(request, game_id):
    game = Game.objects.get(pk=game_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        rating_form = RatingForm(request.POST)

        if review_form.is_valid() and rating_form.is_valid():
            review = review_form.save(commit=False)
            review.game = game
            review.user = request.user  # Associate the review with the logged-in user
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

    
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            favorite_genres = form.cleaned_data['favorite_genres']

            # Create a new user and save to the database
            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, user_name=user_name, password=password)
            user.favorite_genres.set(favorite_genres)

            # Redirect to a success page or login page
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'gameReview_app/user_registration_form.html', {'form': form})

def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page
            return redirect('success_page')
    else:
        form = PublisherForm()

    return render(request, 'publisher_form.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the home page or another appropriate page
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})
