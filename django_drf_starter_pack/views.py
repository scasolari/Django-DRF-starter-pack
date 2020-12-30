from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_paginated_response(self, data):
        return Response(data[0])

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
