from django import forms
from .models import Game, Genre, Publisher, Review, Rating

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
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

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        
class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['game', 'overall_rating']
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

