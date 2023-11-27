from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Game, Review, Rating, Genre, Publisher, User

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

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        if User.objects.filter(user_name=user_name).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return user_name
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered. Please use a different one.")
        return email
    
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

class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['game', 'user', 'overall_rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'overall_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
        }

class EditRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['game', 'review', 'overall_rating']
        widgets = {
            'gameplay_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'graphics_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'sound_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'story_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
        }