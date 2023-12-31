from rest_framework import permissions, viewsets

from profiles import serializers
from profiles import models


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]

