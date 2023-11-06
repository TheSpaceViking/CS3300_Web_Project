from django import forms
from .models import Game, Genre, Publisher, Review, Rating

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'

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
        exclude = ['game', 'review']
        widgets = {
            'overall_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'gameplay_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'graphics_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'sound_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'story_rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
        }

