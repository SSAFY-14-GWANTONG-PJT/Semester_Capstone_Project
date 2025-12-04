from rest_framework import serializers
from .models import Story, Question, Choice

# 가장 작은 단위
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Choice
        fields = ['id', 'question_id', 'content', 'is_correct']
        read_only_fields = ['question_id']

# 조회용 
class QuestionSerializer(serializers.ModelSerializer):
    # 선택지 조회 해서 오기
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta : 
        model = Question
        fields = ['id', 'story_id', 'question', 'choices']
        read_only_fields = ['story_id']

class StorySerializer(serializers.ModelSerializer):
    # 문제 조회해 오기
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta : 
        model = Story
        fields = ['id', 'author_id', 'title', 'content', 'genre', 'story_level', 'like', 'created_at', 'questions']

        