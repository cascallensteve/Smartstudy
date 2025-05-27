from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Register 'myap' app URLs at the root
    path("__reload__/", include("django_browser_reload.urls")),  # For live reload
]
