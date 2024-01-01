from rest_framework import permissions, viewsets
from rest_framework.response import Response

from caching import invalidatable_cache
from profiles import serializers
from profiles import models


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        @invalidatable_cache('user')
        def serialization():
            this_data = self.get_serializer(queryset, many=True)
            return this_data.data
        data = serialization()

        return Response(data)

