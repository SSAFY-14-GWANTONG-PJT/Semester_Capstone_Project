from rest_framework import serializers
from .models import Story, StoryPage, Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Choice
        fields = ['id', 'question', 'content', 'is_correct']
        read_only_fields = ['question']

class QuestionSerializer(serializers.ModelSerializer):
    # 선택지 조회 해서 오기
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta : 
        model = Question
        fields = ['id', 'story', 'question', 'choices']
        read_only_fields = ['story']

class StoryPageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = StoryPage
        fields = ['id', 'page_number', 'content', 'image_data']

class StoryListSerializer(serializers.ModelSerializer):
    # 목록 조회용(커뮤니티에 동화 보기)
    # 닉네임 뽑아오기
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)

    # 썸네일 뽑아오기
    thumbnail = serializers.SerializerMethodField()

    class Meta :
        model = Story
        fields = ['id', 'author_nickname', 'title', 'summary', 'genre', 'story_level', 'like_count', 'created_at', 'thumbnail', 'status']
    
    def get_thumbnail(self, obj) : 
        first_page = obj.pages.first()
        if first_page :
            return first_page.image_data
        return None

class StoryDetailSerializer(serializers.ModelSerializer):
    # 상세 조회용 (페이지 포함)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    pages = StoryPageSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = [
            'id', 'author', 'author_nickname', 'study_set',
            'title', 'summary', 'genre', 'keywords', 
            'story_level', 'like_count', 'status', 'created_at',
            'pages', 'questions'
        ]

class StoryCreateSerializer(serializers.ModelSerializer):
    # 동화 생성용
    class Meta :
        model = Story
        fields = ['title', 'genre', 'story_level', 'keywords', 'study_set']