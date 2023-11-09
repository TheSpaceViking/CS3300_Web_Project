from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Game, Review, Rating, Genre, Publisher

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    user_name = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    favorite_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Favorite Genres'
    )
    
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        exclude = ['overall_rating']
        labels = {
            'title': 'Title',
            'cover_image': 'Cover Image',
            'genre': 'Genre',
            'publisher': 'Publisher',
            'release_year': 'Release Year',
            'platforms': 'Platforms',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'genre': forms.CheckboxSelectMultiple(),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'release_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'platforms': forms.CheckboxSelectMultiple(),
        }
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['game', 'user', 'overall_rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),  # Adjust the 'rows' attribute to control the number of visible rows
            'overall_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
        }
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['game', 'review', 'overall_rating']
        widgets = {
            'gameplay_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'graphics_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'sound_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'story_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
        }
        
class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'website', 'contact']