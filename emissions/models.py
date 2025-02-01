from django.db import models
from django.contrib.auth.models import User
class EmissionFactor(models.Model):
    activity_name = models.CharField(max_length=100)  # e.g., "Car travel"
    emission_factor = models.FloatField()  # Factor (e.g., kg CO₂/unit)

    def __str__(self):
        return self.activity_name

class Activity(models.Model):
    name = models.CharField(max_length=255, default="Default Activity Name")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class EmissionRecord(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name="records")
    emission_factor = models.ForeignKey('EmissionFactor', on_delete=models.CASCADE, related_name="records")
    quantity = models.FloatField(help_text="Amount of activity (e.g., km, kWh)")
    calculated_emissions = models.FloatField(null=True, blank=True, help_text="Calculated emissions in kg CO2")

    def calculate_emissions(self):
    # Calculate the emissions based on the quantity and emission factor
     self.calculated_emissions = self.quantity * self.emission_factor.emission_factor


    def save(self, *args, **kwargs):
     self.calculate_emissions()  # Calculate emissions without triggering save
     super().save(*args, **kwargs)  # Save the instance
class TravelRecord(models.Model):
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    transport_mode = models.CharField(max_length=50)
    emissions = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    activity_value = models.FloatField()
    unit = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    environmental_factor = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.activity_type} - {self.activity_value} {self.unit}"