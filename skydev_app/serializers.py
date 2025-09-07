from rest_framework import serializers
from .models import Domain, Vacancy, VacancyReq


class DomainSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = Domain
        fields = ('name', 'value', 'code')


class VacancySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = Vacancy
        fields = ('id', 'name', 'status', 'region', 'town', 'address')


class VacancyReqSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = VacancyReq
        fields = ('id', 'vacancy', 'whois', 'duties', 'requirements')

