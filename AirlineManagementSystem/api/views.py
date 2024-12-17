from rest_framework import status
from rest_framework.response import Response

from AirlineManagementSystem.models import Airplane, Flight, Reservation
from AirlineManagementSystem.api.serializers import AirplaneSerializer, FlightSerializer, ReservationSerializer

from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class AirplaneListCreateAPIView(APIView):

    def get(self, request):
        airplanes = Airplane.objects.filter(status=True)
        serializer = AirplaneSerializer(airplanes, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = AirplaneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AirplaneDetailAPIView(APIView):

    def get_object(self, pk):
        airplane = get_object_or_404(Airplane, pk=pk)
        return airplane

    def get(self, request, id):
        airplane = self.get_object(pk=id)
        serializer = AirplaneSerializer(airplane)
        return Response(serializer.data)

    def patch(self, request, id):
        airplane = self.get_object(pk=id)
        serializer = AirplaneSerializer(airplane, data=request.data, partial=True)
        if serializer.is_valid():
            flights = airplane.flights.all()
            for flight in flights:
                reservations = flight.reservations.all()
                for reservation in reservations:
                    reservation.status = serializer.validated_data.get("status")
                    reservation.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        airplane = self.get_object(pk=id)
        airplane.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightsOfAirplaneListAPIView(APIView):

    def get_object(self, pk):
        airplane = get_object_or_404(Airplane, pk=pk)
        return airplane

    def get(self, request, id):
        airplane = self.get_object(pk=id)
        flights = Flight.objects.filter(airplane=airplane)
        serializer = FlightSerializer(flights, many=True, context={"request": request})
        return Response(serializer.data)


class FlightsListCreateAPIView(APIView):

    def get(self, request):
        flights = Flight.objects.filter(airplane__status=True).all()
        serializer = FlightSerializer(flights, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            airplane = serializer.validated_data.get("airplane")
            if airplane.status:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("A flight cannot be added to a plane whose status is false",
                                status=status.HTTP_403_FORBIDDEN, )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightDetailAPIView(APIView):

    def get_object(self, pk):
        flight = get_object_or_404(Flight, pk=pk)
        return flight

    def get(self, request, id):
        flight = self.get_object(pk=id)
        serializer = FlightSerializer(flight)
        return Response(serializer.data)

    def patch(self, request, id):
        flight = self.get_object(pk=id)
        serializer = FlightSerializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        flight = self.get_object(pk=id)
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationsOfFlightListAPIView(APIView):

    def get_object(self, pk):
        flight = get_object_or_404(Flight, pk=pk)
        return flight

    def get(self, request, id):
        flight = self.get_object(pk=id)
        reservations = Reservation.objects.filter(flight=flight)
        serializer = ReservationSerializer(reservations, many=True, context={"request": request})
        return Response(serializer.data)


class ReservationListCreateAPIView(APIView):

    def get(self, request):
        reservations = Reservation.objects.filter(status=True)
        serializer = ReservationSerializer(reservations, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            flight = serializer.validated_data.get("flight")
            airplane = Airplane.objects.filter(pk=flight.airplane_id).get()
            if not airplane.status:
                return Response("A reservation cannot be added to a plane whose 'status' is false",
                                status=status.HTTP_403_FORBIDDEN)
            reservations_counter = Reservation.objects.all().filter(flight=flight.id, status=True).count()
            capacity = airplane.capacity
            if capacity > reservations_counter:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("The flights's capacity is full", status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetailAPIView(APIView):

    def get_object(self, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        return reservation

    def get(self, request, id):
        reservation = self.get_object(pk=id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def patch(self, request, id):
        reservation = self.get_object(pk=id)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            if "flight" in serializer.validated_data:
                new_flight = serializer.validated_data.get("flight")
                new_airplane = new_flight.airplane
                new_airplane_status = new_airplane.status
            else:
                new_flight = reservation.flight
                new_airplane = reservation.flight.airplane
                new_airplane_status = new_airplane.status

            if "status" in serializer.validated_data:
                new_status = serializer.validated_data.get("status")
            else:
                new_status = reservation.status

            if(new_airplane_status == False):
                return Response("The entered flight's airplane 'status' is false", status=status.HTTP_403_FORBIDDEN)
            if new_status == False:
                reservation_number = Reservation.objects.all().filter(flight=new_flight).count()
                if new_airplane.capacity > reservation_number:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("The entered flight's capacity is full",
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            elif new_status == True:
                if new_airplane_status == True:
                    reservation_number = Reservation.objects.all().filter(flight=new_flight).count()
                    if new_airplane.capacity > reservation_number:
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response("The entered flight's capacity is full",
                                        status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response("The entered flight's airplane 'status' is false", status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        reservation = self.get_object(pk=id)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
