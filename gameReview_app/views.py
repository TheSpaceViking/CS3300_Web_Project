
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Game, Platform, Genre, User, Publisher, Review
from .forms import ReviewForm, GameForm, UserRegistrationForm, PublisherForm, RatingForm, EditReviewForm, EditRatingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages

def index(request):
    games = Game.objects.all()

    if request.user.is_authenticated:
        user_genres = request.user.favorite_genres.all()
        if user_genres.count() > 0:
            games = Game.objects.filter(Q(genre__in=user_genres) | Q(genre__isnull=True)).distinct()

    latest_reviews = Review.objects.filter(game__in=games, created_at__gte=timezone.now() - timezone.timedelta(days=1))
    games_with_newest_reviews = sorted(set(review.game for review in latest_reviews), key=lambda game: max(review.created_at for review in latest_reviews if review.game == game), reverse=True)

    return render(request, 'gameReview_app/index.html', {'games': games_with_newest_reviews})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login successful')  # Add this line for debugging
        return super().form_valid(form)

@login_required
def user_profile(request):
    return render(request, 'index.html')

def redirect_to_index(request):
    return redirect('index')

def game_list(request):
    games = Game.objects.all()
    return render(request, 'gameReview_app/game_list.html', {'games': games})

def game_detail(request, game_id):
    game = Game.objects.get(pk=game_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.game = game
            review.save()
            return redirect('game_detail', game_id=game_id)
    else:
        review_form = ReviewForm()

    return render(request, 'gameReview_app/game_detail.html', {'game': game, 'review_form': review_form})

def platform_list(request):
    platforms = Platform.objects.all()
    return render(request, 'gameReview_app/platform_list.html', {'platforms': platforms})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'gameReview_app/genre_list.html', {'genres': genres})

@login_required
def add_game(request):
    publishers = Publisher.objects.all()

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            selected_genres = request.POST.getlist('genre')
            selected_platforms = request.POST.getlist('platforms')

            game.save()
            game.genre.set(selected_genres)
            game.platforms.set(selected_platforms)

            publisher_id = request.POST.get('publisher')
            if publisher_id:
                publisher = Publisher.objects.get(pk=publisher_id)
                game.publisher = publisher

            game.save()

            messages.success(request, 'Game added successfully.')
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm()

    return render(request, 'gameReview_app/game_form.html', {'form': form, 'publishers': publishers})

@login_required
def create_review(request, game_id):
    game = Game.objects.get(pk=game_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        rating_form = RatingForm(request.POST)

        if review_form.is_valid() and rating_form.is_valid():
            review = review_form.save(commit=False)
            review.game = game
            review.user = request.user
            review._request = request  # Pass the request object to the save method
            review.save()

            rating = rating_form.save(commit=False)
            rating.game = game
            rating.review = review
            rating.save()

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

            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, user_name=user_name, password=password)
            user.favorite_genres.set(favorite_genres)

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'gameReview_app/user_registration_form.html', {'form': form})

def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = PublisherForm()

    return render(request, 'publisher_form.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def search_results(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text', '')
        
        # Filter games by title or genre, and select distinct titles
        games = Game.objects.filter(Q(title__icontains=search_text) | Q(genre__game_genre__icontains=search_text)).distinct()
        
        return render(request, 'gameReview_app/search_results.html', {'games': games})
    
    return render(request, 'gameReview_app/search_results.html')

def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.user == game.publisher.user:
        game.delete()
        return redirect('index')

def delete_review(request, game_id, review_id):
    game = get_object_or_404(Game, id=game_id)
    review = get_object_or_404(Review, id=review_id)

    if request.user == review.user:
        # Delete the associated rating
        rating = review.review_ratings
        if rating:
            rating.delete()

        # Delete the review
        review.delete()

        # Recalculate the game's overall rating
        game.calculate_overall_average_rating()
        game.save()

        return redirect('game_detail', game_id=game.id)
    
def edit_review(request, game_id, review_id):
    game = get_object_or_404(Game, id=game_id)
    review = get_object_or_404(Review, id=review_id, game=game, user=request.user)

    if request.method == 'POST':
        review_form = EditReviewForm(request.POST, instance=review)
        rating_form = EditRatingForm(request.POST, instance=review.review_ratings)

        if review_form.is_valid() and rating_form.is_valid():
            review_form.save()
            rating_form.save()

            # Recalculate the game's overall rating
            game.calculate_overall_average_rating()
            game.save()

            return redirect('game_detail', game_id=game_id)
    else:
        review_form = EditReviewForm(instance=review)
        rating_form = EditRatingForm(instance=review.review_ratings)

    return render(request, 'gameReview_app/edit_review_form.html', {
        'game': game,
        'review_form': review_form,
        'rating_form': rating_form,
    })    

def review_detail(request, game_id, review_id):
    game = get_object_or_404(Game, id=game_id)
    review = get_object_or_404(Review, id=review_id)

    context = {
        'game': game,
        'review': review,
    }

    return render(request, 'gameReview_app/review_detail.html', context)