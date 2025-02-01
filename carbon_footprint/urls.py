from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Example view for the root path
def home_view(request):
    return HttpResponse("<h1>Welcome to the Carbon Footprint App</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('emissions.urls')),  # Include the emissions app URLs
]
