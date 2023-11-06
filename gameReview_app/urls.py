from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('platforms/', views.platform_list, name='platform_list'),
    path('genres/', views.genre_list, name='genre_list'),
    path('create_review/<int:game_id>/', views.create_review, name='create_review'),
]
