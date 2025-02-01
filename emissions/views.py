from rest_framework import viewsets
from .models import EmissionFactor, Activity, EmissionRecord,UserActivity
from .serializer import EmissionFactorSerializer, ActivitySerializer, EmissionRecordSerializer,EmissionsSerializer,UserActivitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
class EmissionFactorViewSet(viewsets.ModelViewSet):
    queryset = EmissionFactor.objects.all()
    serializer_class = EmissionFactorSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
class EmissionRecordViewSet(viewsets.ModelViewSet):
    queryset = EmissionRecord.objects.all()
    serializer_class = EmissionRecordSerializer


# Emission factors (grams per km)
EMISSION_FACTORS = {
    'car': 150,
    'bus': 60,
    'train': 50,
    'flight': 200
}

class CalculateEmissions(APIView):
    def post(self, request):
        serializer = EmissionsSerializer(data=request.data)
        if serializer.is_valid():
            start_location = serializer.validated_data['startLocation']
            end_location = serializer.validated_data['endLocation']
            transport_mode = serializer.validated_data['transportMode']

            # Call Google Maps API to get the distance
            distance = self.get_distance(start_location, end_location)

            # Calculate emissions
            emissions = distance * EMISSION_FACTORS.get(transport_mode, 0)

            return Response({'emissions': emissions})
        else:
            return Response(serializer.errors, status=400)

    def get_distance(self, start, end):
        # Set up Google Maps API (you should replace YOUR_GOOGLE_MAPS_API_KEY with your actual API key)
        api_key = 'AIzaSyC3R7y2ficboVL5_hCuUtBgqEcMmWb3yYw'
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&key={api_key}'
        response = requests.get(url).json()

        # Extract distance in kilometers
        if response['status'] == 'OK':
            distance = response['routes'][0]['legs'][0]['distance']['value'] / 1000  # distance in km
            return distance
        else:
            return 0
class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        activity_data = request.data
        activity_data['user'] = user.id  # Automatically associate activity with the logged-in user

        serializer = self.get_serializer(data=activity_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)