from django.test import TestCase, Client
from .models import Booking, TravelOption
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your tests here.


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@test.com", password="password123")


    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
    
    def test_login_fail(self):
        response = self.client.post(reverse('login'), {'username': 'wrong', 'password':'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "❌ Invalid username or password.")


class TravelOptionModelTest(TestCase):
    def setUp(self):
        self.option = TravelOption.objects.create(
            type="flight",
            source="Jakarta",
            destination="Bali",
            date_and_time=timezone.now(),
            price=100,
            available_seats=50
        )

    def test_travel_option_str(self):
        self.assertEqual(str(self.option), f"flight from Jakarta to Bali on {self.option.date_and_time}")



class BookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.option = TravelOption.objects.create(
            type="flight",
            source="Jakarta",
            destination="Bali",
            date_and_time=timezone.now(),
            price=100,
            available_seats=50
        )

    def test_booking_creation(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse('book', kwargs={'pk': self.option.id}), {
            'number_of_seats': 2
        })
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.travel_option, self.option)
        self.assertEqual(booking.total_price, 200)
        self.assertEqual(booking.status, 'confirmed')
