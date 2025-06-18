from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScriptViewSet

# Create a router and register our viewsets with it.
# The DefaultRouter automatically generates the URL patterns for the viewset.
# This will create routes for list, create, retrieve, update, partial_update, and destroy actions.
# e.g., /api/scripts/ and /api/scripts/<pk>/
router = DefaultRouter()
router.register(r'scripts', ScriptViewSet, basename='script')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
