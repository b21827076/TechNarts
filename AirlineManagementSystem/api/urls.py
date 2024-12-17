from django.urls import path
from AirlineManagementSystem.api import views as api_views

urlpatterns = [
    path('airplanes/', api_views.AirplaneListCreateAPIView.as_view(), name='airplanes_list'),
    path('airplanes/<int:id>/', api_views.AirplaneDetailAPIView.as_view(), name='airplane_detail'),
    path('airplanes/<int:id>/flights/', api_views.FlightsOfAirplaneListAPIView.as_view(), name='flights_of_airplane_list'),

    path('flights/', api_views.FlightsListCreateAPIView.as_view(), name = 'flights_list'),
    path('flights/<int:id>/', api_views.FlightDetailAPIView.as_view(), name='flight_detail'),
    path('flights/<int:id>/reservations/', api_views.ReservationsOfFlightListAPIView.as_view(), name='reservations_of_flight_list'),

    path('reservations/', api_views.ReservationListCreateAPIView.as_view(), name='reservations_list'),
    path('reservations/<int:id>/', api_views.ReservationDetailAPIView.as_view(), name='reservation_detail'),
]
