from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Story, StoryPage, Question, Choice
from .serializers import (
    StoryListSerializer, 
    StoryDetailSerializer, 
    StoryCreateSerializer, 
    QuestionSerializer,
    StoryPageSerializer,
    ChoiceSerializer
)
# Create your views here.

# 동화 리스트 불러들이기, 동화 만들기
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def story_list_create(request) :
    if request.method == 'GET' :   
        # 최신 순 불러들이기
        queryset = Story.objects.all().order_by('-created_at')

        # 필터링
        genre = request.query_params.get('genre')
        level = request.query_params.get('level')
        if genre:
            queryset = queryset.filter(genre=genre)
        if level:
            queryset = queryset.filter(story_level=level)
            
        serializer = StoryListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST' : # GEMINI 생성 이후 날릴 요청
        serializer = StoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 동화 상세 조회 및 수정
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)

    if request.method == 'GET': 
        serializer = StoryDetailSerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if story.author != request.user : # 만약 스토리 작성자와 요청자 다르면 안되게
            return Response({'error' : '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
        
        # 동화 작성자와 요청자 같다면 수정, 
        # 여기서 status를 변경할 시 DELETE 역할도 할 것이라 DELETE 따로 작성 X
        serializer = StoryDetailSerializer(story, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 동화 페이지 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def story_page_list_create(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if request.method == 'GET':
        pages = StoryPage.objects.filter(story=story)
        serializer = StoryPageSerializer(pages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 해당 동화에 페이지 추가
        serializer = StoryPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(story=story)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 문제 목록 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def story_question_list_create(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if request.method == 'GET':
        questions = Question.objects.filter(story=story)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(story=story)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 문제에 딸린 선택지(보기) 생성 및 추가
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def question_choice_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(question=question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
