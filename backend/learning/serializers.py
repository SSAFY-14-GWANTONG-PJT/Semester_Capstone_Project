from rest_framework import serializers
from .models import Voca, StudySet, Meaning


class MeaningSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Meaning
        fields = ['id', 'content', 'part']
        
        
class VocaSerializer(serializers.ModelSerializer):
    
    meanings = MeaningSerializer(many=True, read_only=True)
    
    class Meta:
        model = Voca
        fields = ['id', 'level', 'word', 'cefr_band', 'meanings']
        

class StudySetSerializer(serializers.ModelSerializer):
    vocas = VocaSerializer(many=True, read_only=True)

    class Meta:
        model = StudySet
        fields = ['level', 'unit_number', 'vocas']