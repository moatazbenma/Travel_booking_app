from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class TravelOption(models.Model):
    options = [
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    ]
    type = models.CharField(choices=options, max_length=50)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_and_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.type} from {self.source} to {self.destination} on {self.date_and_time}"
    



class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey('TravelOption', on_delete=models.CASCADE)
    number_of_seats = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='confirmed')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.travel_option} ({self.status})"