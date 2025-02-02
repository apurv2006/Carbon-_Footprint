from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmissionFactorViewSet, ActivityViewSet, EmissionRecordViewSet, CalculateEmissions,UserActivityViewSet
from . import views
router = DefaultRouter()
router.register(r'factors', EmissionFactorViewSet, basename='emission-factors')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'emission-records', EmissionRecordViewSet)
router.register(r'user-activity', UserActivityViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('calculate-emissions/', CalculateEmissions.as_view(), name='calculate_emissions'),
   path('predict/', views.predict_carbon_emission, name='predict_carbon_emission'),
   path('submit-carbon-footprint/', views.submit_carbon_footprint, name='submit_carbon_footprint'),
    # path('past-predictions/', PastPredictionsView.as_view(), name='pasy-predictions'),
]
