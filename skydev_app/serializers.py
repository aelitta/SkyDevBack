from rest_framework import serializers
from .models import Domain


class DomainSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = Domain
        fields = ('name', 'value', 'code')