from rest_framework import serializers
from .models import EmissionFactor, Activity, EmissionRecord,UserActivity,Prediction

class EmissionFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionFactor
        fields = ['id', 'activity_type', 'emission_factor']

class ActivitySerializer(serializers.ModelSerializer):
    total_emissions = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'name', 'activity_data', 'emission_factor', 'timestamp', 'total_emissions']

    def get_total_emissions(self, obj):
        return obj.calculate_emissions()
class EmissionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionRecord
        fields = ['id', 'activity', 'emission_factor', 'quantity', 'calculated_emissions']
class EmissionsSerializer(serializers.Serializer):
    startLocation = serializers.CharField(max_length=200)
    endLocation = serializers.CharField(max_length=200)
    transportMode = serializers.ChoiceField(choices=['car', 'bus', 'train', 'flight'])
class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['user', 'activity_type', 'activity_value', 'unit', 'timestamp', 'environmental_factor']
class PredictionSerializer(serializers.Serializer):
    vehicle_distance = serializers.FloatField()
    grocery_bill = serializers.FloatField()
    waste_bag_count = serializers.IntegerField()
    predicted_emission = serializers.FloatField()
    suggestions = serializers.ListField(child=serializers.CharField())
    def create(self, validated_data):
        # Create a new CarbonFootprint instance and save to the database
        return Prediction.objects.create(**validated_data)
class CarbonFootprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['vehicle_distance', 'grocery_bill', 'waste_bag_count', 'predicted_emission', 'suggestions']

    def create(self, validated_data):
        # Create a new CarbonFootprint instance and save to the database
        return Prediction.objects.create(**validated_data)
