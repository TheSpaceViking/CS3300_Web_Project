from django.urls import path, include
from gameReview_app.views import CustomLoginView, search_results, review_detail
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('game_list/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('platforms/', views.platform_list, name='platform_list'),
    path('genres/', views.genre_list, name='genre_list'),
    path('add_game/', views.add_game, name='add_game'),
    path('create_review/<int:game_id>/', views.create_review, name='create_review'),
    path('add_publisher/', views.add_publisher, name='add_publisher'),
    path('register/', views.user_registration, name='user_registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.redirect_to_index, name='profile_redirect'),
    path('search_results/', search_results, name='search_results'),
    path('delete_game/<int:game_id>/', views.delete_game, name='delete_game'),
    path('delete_review/<int:game_id>/<int:review_id>/', views.delete_review, name='delete_review'),
    path('edit_review/<int:game_id>/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/<int:game_id>/<int:review_id>/', review_detail, name='review_detail'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
