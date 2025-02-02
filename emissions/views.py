from rest_framework import viewsets
from .models import EmissionFactor, Activity, EmissionRecord,UserActivity
from .serializer import EmissionFactorSerializer, ActivitySerializer, EmissionRecordSerializer,EmissionsSerializer,UserActivitySerializer,PredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import JsonResponse
from .models import Prediction

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
import joblib
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
model_pipeline = joblib.load('C:/Users/apurva vivobook/Desktop/code/model/carbon_emission_model.pkl')

# Define the prediction logic
def suggest_personalized_action(user_data, predicted_emission):
    # Example benchmarks for the carbon footprint
    average_vehicle_distance = 500  # Average vehicle distance per month (km)
    average_grocery_bill = 500  # Average monthly grocery bill
    average_waste_bag_count = 5  # Average number of waste bags per week

    suggestions = []

    if int(user_data['Vehicle Monthly Distance Km'])> average_vehicle_distance:
        suggestions.append("You can reduce your carbon footprint by using public transportation or carpooling more frequently.")
    else:
        suggestions.append("Great job! You're already minimizing your vehicle usage.")

    if int(user_data['Monthly Grocery Bill']) > average_grocery_bill:
        suggestions.append("Consider buying in bulk and reducing food waste to lower your grocery-related emissions.")
    else:
        suggestions.append("Your grocery consumption is already sustainable. Keep it up!")

    if int(user_data['Waste Bag Weekly Count']) > average_waste_bag_count:
        suggestions.append("Try to reduce your waste production by composting and recycling more.")
    else:
        suggestions.append("Good job! Your waste management practices are already environmentally friendly.")

    if predicted_emission > 3000:
        suggestions.append("Your carbon footprint is quite high. Consider integrating energy-efficient practices in your daily routine.")
    elif 1500 < predicted_emission <= 3000:
        suggestions.append("Your carbon footprint is moderate. Some lifestyle changes like reducing car usage could help.")
    else:
        suggestions.append("Awesome! Your carbon footprint is low. Keep maintaining these sustainable practices.")

    return suggestions

@api_view(['POST'])
def predict_carbon_emission(request):
    # Get data from the frontend (React)
    user_data = request.data
    selected_features = ['Vehicle Monthly Distance Km', 'Monthly Grocery Bill', 'Waste Bag Weekly Count']

    # Prepare the data for prediction (same preprocessing as in the training phase)
    df_selected = pd.DataFrame([user_data], columns=selected_features)
    df_selected_encoded = pd.get_dummies(df_selected, drop_first=True)
    file_path = 'C:/Users/apurva vivobook/Desktop/code/model/X_train_columns.csv'
    # Load the training columns (ensure the model expects the same columns)
    X_train_columns = pd.read_csv(file_path, header=None).squeeze().tolist()
    df_selected_encoded = df_selected_encoded.reindex(columns=X_train_columns, fill_value=0)

    # Predict emissions
    predicted_emission = model_pipeline.predict(df_selected_encoded)[0]

    # Get personalized suggestions based on the predicted emissions
    suggestions = suggest_personalized_action(user_data, predicted_emission)

    # Prepare response data
    response_data = {
        'predicted_emission': predicted_emission,
        'suggestions': suggestions
    }

    return Response(response_data)
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializer import PredictionSerializer
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def submit_carbon_footprint(request):
    if request.method == 'POST':
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the data to MySQL
            
            # Prepare the JsonResponse with the success message
            response = JsonResponse({'message': 'Data saved successfully!'})
            response['Access-Control-Allow-Origin'] = '*'  # Set CORS header to allow any origin
            
            return response  # Return the response
        else:
            # Log the validation errors for debugging
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PastPredictionsView(APIView):
    def get(self, request):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)