from rest_framework import viewsets, permissions, parsers
from .models import Script
from .serializers import ScriptSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete objects.
    All users (including anonymous) can read (GET, HEAD, OPTIONS) objects.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff


class ScriptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scripts to be viewed or edited.

    - Provides full CRUD (Create, Retrieve, Update, Delete) functionality.
    - Public users can view the list of scripts and individual script details.
    - Only admin users can create, update, or delete scripts. This is controlled
      by the `IsAdminOrReadOnly` permission class. This endpoint would be used
      by the admin panel or a secure tool like a Telegram bot with admin credentials.
    - The bot will send data as 'multipart/form-data' so we add the parser.
    """
    queryset = Script.objects.filter(is_active=True)
    serializer_class = ScriptSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
