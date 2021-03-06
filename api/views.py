from datetime import timedelta, datetime
from django.conf import settings
import urllib
import json
from django.db.models import Q

from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import generics, mixins, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token
from api.serializers import UserSerializer
from main.models import User
from main import models
from main.serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer
from . import serializers
from django.core.mail import EmailMessage


class AuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class ListUser(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class ApplicationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('approved',)
    queryset = models.Application.objects.all().order_by('-timestamp')

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.type == User.CLIENT:
            return models.Application.objects.filter(user=self.request.user).order_by('-timestamp')
        return models.Application.objects.all().order_by('-timestamp')

    def get_serializer_class(self):
        if self.action == 'create_application':
            return ApplicationCreateSerializer
        if self.action == 'update_application':
            return ApplicationUpdateSerializer
        return ApplicationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticated]
        if self.action == "add_lesson":
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False)
    def create_application(self, request, *args, **kwargs):
        serializer = ApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_application = models.Application.objects.create(money=request.data["money"], user=request.user)
            return Response(self.get_serializer(new_application, many=False).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def update_application(self, request, *args, **kwargs):
        serializer = ApplicationUpdateSerializer(data=request.data)
        application = models.Application.objects.get(pk=request.data["pk"])
        if serializer.is_valid():
            application.noticed = True
            application.save()
            return Response(self.get_serializer(application, many=False).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
