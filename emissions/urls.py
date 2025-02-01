from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmissionFactorViewSet, ActivityViewSet, EmissionRecordViewSet, CalculateEmissions

router = DefaultRouter()
router.register(r'factors', EmissionFactorViewSet, basename='emission-factors')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'emission-records', EmissionRecordViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('calculate-emissions/', CalculateEmissions.as_view(), name='calculate_emissions'),
]