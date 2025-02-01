from rest_framework import serializers
from .models import EmissionFactor, Activity, EmissionRecord,UserActivity

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