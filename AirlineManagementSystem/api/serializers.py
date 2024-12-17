from rest_framework import serializers
from AirlineManagementSystem.models import Airplane, Flight, Reservation


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"
        read_only_fields = ["id"]


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"
        read_only_fields = ["id"]



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ["id", "reservation_code", "created_at"]

class ReservationPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ["id", "reservation_code", "created_at"]
