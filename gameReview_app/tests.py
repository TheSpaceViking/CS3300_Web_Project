from django.test import TestCase
from .models import Genre, User, Platform, Publisher, Game, Rating, Review
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelTestCase(TestCase):
    def setUp(self):
        # Create sample objects for testing
        self.genre = Genre.objects.create(game_genre='Action')
        self.platform = Platform.objects.create(name='PlayStation 5')
        self.publisher = Publisher.objects.create(name='Sample Publisher', website='http://example.com', contact='John Doe')
        self.user = User.objects.create(email='user@example.com', first_name='John', last_name='Doe', user_name='johndoe')
        self.game = Game.objects.create(title='Sample Game', publisher=self.publisher, release_year='2022-01-01')
        self.review = Review.objects.create(title='Sample Review', user=self.user, game=self.game, content='Great game!')
        self.rating = Rating.objects.create(review=self.review, gameplay_rating=4.5, graphics_rating=4.5, sound_rating=4.5, story_rating=4.5)
    
    def test_genre_str(self):
        self.assertEqual(str(self.genre), 'Action')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'johndoe')

    def test_platform_str(self):
        self.assertEqual(str(self.platform), 'PlayStation 5')

    def test_publisher_str(self):
        self.assertEqual(str(self.publisher), 'Sample Publisher')

    def test_game_str(self):
        self.assertEqual(str(self.game), 'Sample Game')

    def test_review_str(self):
        self.assertEqual(str(self.review), 'Sample Review - Sample Game')

    def test_rating_str(self):
        self.assertEqual(str(self.rating), 'Sample Review - Sample Game rating')

class SignalTestCase(TestCase):
    def setUp(self):
        # Create sample objects for testing
        self.user = User.objects.create(email='user@example.com', first_name='John', last_name='Doe', user_name='johndoe')
        self.game = Game.objects.create(title='Sample Game', release_year='2022-01-01')
        self.review = Review.objects.create(title='Sample Review', game=self.game, content='Great game!')
        self.rating = Rating.objects.create(review=self.review, gameplay_rating=4.5, graphics_rating=4.5, sound_rating=4.5, story_rating=4.5)
    
    def test_update_review_on_rating_save(self):
        # Ensure overall rating of the review is updated when a rating is saved
        new_rating = Rating.objects.create(review=self.review, gameplay_rating=4.0, graphics_rating=4.0, sound_rating=4.0, story_rating=4.0)
        new_rating.save()
        self.review.refresh_from_db()
        self.assertEqual(self.review.overall_rating, 4.0)


    def test_update_review_overall_rating(self):
        # Ensure overall rating of the review is updated when a review is saved
        new_rating = Rating.objects.create(review=self.review, gameplay_rating=4.0, graphics_rating=4.0, sound_rating=4.0, story_rating=4.0)
        new_rating.save()
        self.review.refresh_from_db()
        self.assertEqual(self.review.overall_rating, 4.0)

class ViewTestCase(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(email='testuser@example.com', first_name='Test', last_name='User', user_name='testuser', password='testpassword')
        self.publisher = Publisher.objects.create(name='Test Publisher', website='http://example.com', contact='John Doe')

    def test_add_game_form_displayed(self):
        # Ensure the add game form is displayed for a logged-in user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_game'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'gameReview_app/game_form.html')
        self.assertContains(response, 'Add a New Game')
        self.assertContains(response, 'Publisher')
        self.assertContains(response, 'Title')

    def test_add_game_success(self):
        # Ensure a new game is created upon successful form submission
        self.client.login(username='testuser', password='testpassword')
        #image = SimpleUploadedFile('cover_image.jpg', b'file_content', content_type='image/jpeg')
        post_data = {
            'title': 'New Game',
            'release_year': '2022-01-01',
            'genre': [1],  # Assuming 1 is a valid genre ID
            'platforms': [1],  # Assuming 1 is a valid platform ID
            'publisher': self.publisher.id,
            #'cover_image': image
        }
        
        response = self.client.post(reverse('add_game'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check if the game was added to the database
        self.assertTrue(Game.objects.filter(title='New Game').exists())


    def test_add_game_requires_authentication(self):
        # Ensure that only authenticated users can access the add game form
        response = self.client.get(reverse('add_game'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('add_game'))

    def test_add_game_invalid_form(self):
        # Ensure that an invalid form submission does not add a game
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'title': '',  # This is intentionally left empty to make the form invalid
            'release_year': '2022-01-01',
            'genre': [1],  # Assuming 1 is a valid genre ID
            'platforms': [1],  # Assuming 1 is a valid platform ID
            'publisher': self.publisher.id,
        }

        response = self.client.post(reverse('add_game'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
