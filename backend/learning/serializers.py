from rest_framework import serializers
from .models import Voca, StudySet

class VocaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voca
        fields = ['id', 'word', 'meaning', 'cefr_band']

class StudySetSerializer(serializers.ModelSerializer):
    vocas = VocaSerializer(many=True, read_only=True)

    class Meta:
        model = StudySet
        fields = ['level', 'unit_number', 'vocas']