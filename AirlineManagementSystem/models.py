import random
import string
from django.db import models

# Create your models here.

class Airplane(models.Model):
    tail_number = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField()
    production_year = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tail_number} ({self.model})"

class Flight(models.Model):
    flight_number = models.CharField(max_length=50)
    departure = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')

    def __str__(self):
        return f"Flight {self.flight_number} from {self.departure} to {self.destination}"

class Reservation(models.Model):
    passenger_name = models.CharField(max_length=50)
    passenger_email = models.EmailField()
    reservation_code = models.CharField(max_length=5,unique=True, editable=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            self.reservation_code = self.generate_unique_reservation_code()
        super().save(*args, **kwargs)

    def generate_unique_reservation_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not Reservation.objects.filter(reservation_code=code).exists():
                return code

    def __str__(self):
        return f"Reservation '{self.reservation_code}' for '{self.passenger_name}' on Flight {self.flight.flight_number}"