from django.contrib import admin
from AirlineManagementSystem.models import Airplane, Flight, Reservation
# Register your models here.

admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Reservation)
