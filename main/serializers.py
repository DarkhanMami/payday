from django.db.models import QuerySet
from rest_framework import serializers

from api.serializers import UserSerializer
from main.models import *


class EmptySerializer(serializers.Serializer):
    pass


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('money',)