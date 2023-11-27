from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from .models import Game, Rating, Review
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

User = get_user_model()

class GameModelTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create(title="Test Game", release_year="2022-01-01")

    def test_game_str(self):
        self.assertEqual(str(self.game), "Test Game")
        
class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(user_name="johndoe", email="test@example.com", first_name="John", last_name="Doe", password="testpass")
        self.game = Game.objects.create(title="Test Game", release_year="2022-01-01")
        self.review = Review.objects.create(title="Test Review", user=self.user, game=self.game, content="This is a test review")

    def test_review_str(self):
        self.assertEqual(str(self.review), "Test Review - Test Game")

class RatingModelTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create(title="Test Game", release_year="2022-01-01")
        self.review = Review.objects.create(title="Test Review", game=self.game)
        self.rating = Rating.objects.create(
            review=self.review,
            overall_rating=4.5,
            gameplay_rating=4.0,
            graphics_rating=5.0,
            sound_rating=4.5,
            story_rating=4.0
        )

    def test_rating_str(self):
        self.assertEqual(str(self.rating), f"{self.review} rating")

    def test_rating_save_updates_review(self):
        # Reload the review from the database to get the updated overall_rating
        self.review.refresh_from_db()
        self.assertEqual(self.review.overall_rating, 4.5)

class UserLoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_user_login(self):
        user = User.objects.create_user(user_name="testuser", email="testuser@example.com", first_name="John", last_name="Doe", password="testpass123")
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        user_name_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        user_name_input.send_keys("testuser")

        password_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("testpass123")
        password_input.send_keys(Keys.RETURN)

        # Wait for the page to load before checking the title
        WebDriverWait(self.selenium, 10).until(
            EC.title_contains("GR4G")
        )

        # Check if the user is redirected to the home page or another expected page after login
        self.assertEqual(self.selenium.title, "GR4G")

class UserRegistrationTest(LiveServerTestCase):  # Change here
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_user_registration(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        user_name_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, "user_name"))
        )
        user_name_input.send_keys("testuser")
        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys("testuser@example.com")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("testpass123")
        password_confirm_input = self.selenium.find_element(By.NAME, "confirm_password")
        password_confirm_input.send_keys("testpass123")
        password_confirm_input.send_keys(Keys.RETURN)

        # Check if the user is redirected to the home page or another expected page after registration
        self.assertEqual(self.selenium.title, "GR4G")

