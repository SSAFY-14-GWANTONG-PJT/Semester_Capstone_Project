from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db import transaction
import requests

from .models import Story, StoryPage, Question, Choice
from .serializers import (
    StoryListSerializer, 
    StoryDetailSerializer, 
    StoryCreateSerializer, 
    QuestionSerializer,
    StoryPageSerializer,
    ChoiceSerializer
)

# AI 서버 주소(docker-compose 서비스 명 'ai' 사용)
AI_SERVER_URL = "http://ai:8000"

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
        story_status = request.query_params.get('status')

        if genre: queryset = queryset.filter(genre=genre)
        if level: queryset = queryset.filter(story_level=level)
        if story_status: queryset = queryset.filter(status=story_status)
            
        serializer = StoryListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST' : # FastAPI로 요청 보내는 Request, 결과 DB에 저장
        
        # Vue로 부터 받은 데이터 정리
        input_data = request.data

    # ai 서버로 보낼 페이로드(FastAPI 내 StoryRequest 따라)
    ai_payload = {
            "age": input_data.get('age', 7),           # 기본값 설정
            "story_level": input_data.get('story_level', 1),
            "genre": input_data.get('genre', 'General'),
            "keywords": input_data.get('keywords', []),
            "vocab_words": input_data.get('vocab_words', []),
            "study_set_id": input_data.get('study_set_id')
        }
    
    # 변수 미리 초기화 (UnboudLocalError 방지목적)
    response = None

    try :
        
        print(f"AI 서버로 동화 생성 요청 전송 : {ai_payload}")

        # AI 서버로 요청
        response = requests.post(f"{AI_SERVER_URL}/generate-story", json=ai_payload)
            
        if response.status_code != 200:
            return Response({'errors': 'AI Story Generation Failed'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        story_data = response.json()
            
        with transaction.atomic():
            new_story = Story.objects.create(
                author=request.user,
                study_set_id=story_data.get('study_set_id'),
                title=story_data.get('title'),
                summary=story_data.get('summary'),
                genre=story_data.get('genre'),
                keywords=story_data.get('keywords'),
                story_level=story_data.get('story_level'),
                status='completed'
            )

            pages_data = story_data.get('pages', [])
            
            for page in pages_data:
                StoryPage.objects.create(
                    story=new_story,
                    page_number=page.get('page_number'),
                    content_en=page.get('content_en'), 
                    content_ko=page.get('content_kr'), # [핵심] AI 응답(content_kr)을 DB(content_ko)에 저장
                    image_data=page.get('image_data')
                    # audio는 null로 저장 (Lazy Loading)
                )

        return Response(StoryDetailSerializer(new_story).data, status=status.HTTP_201_CREATED)
        
    # 만약 AI 서버 연결 실패라면
    except requests.exceptions.RequestException as e :
        print(f"AI 서버 연결 오류 : {e}") 
        return Response(
            {'errors' : 'Cannot connect to AI Service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # 기타 오류라면
    except Exception as e :
        print(f"서버 내부 오류 : {e}")
        return Response(
            {'errors' : 'Error Occured'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_page_tts(request, page_id):
    page = get_object_or_404(StoryPage, pk=page_id)

    if page.audio_en:
        return Response({'audio_en': page.audio_en}, status=status.HTTP_200_OK)

    try:
        tts_payload = {
            "text": page.content_en,
            "voice_name": "Aoede"
        }
        
        # [수정] timeout을 60초로 넉넉하게 설정합니다.
        # AI 서버가 200 OK를 줄 때까지 Django가 끈기 있게 기다리게 합니다.
        response = requests.post(
            f"{AI_SERVER_URL}/generate-tts", 
            json=tts_payload,
            timeout=60 
        )
        
        if response.status_code == 200:
            audio_data = response.json().get('audio_data')
            page.audio_en = audio_data
            page.save()
            return Response({'audio_en': audio_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'AI Server Error'}, status=response.status_code)

    except requests.exceptions.Timeout:
        # 60초가 넘어가도 응답이 없을 때만 타임아웃을 냅니다.
        print(f"페이지 {page_id} TTS 생성 타임아웃 발생")
        return Response({'error': 'TTS 생성 시간이 너무 오래 걸립니다.'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def story_question_list_create(request, story_id) : 
    story = get_object_or_404(Story, pk=story_id)

    if request.method == 'GET' :
        questions = Question.objects.filter(story=story)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 문제 생성
    elif request.method == 'POST' : 
        
        # 동화 본문 텍스트 가져오기
        pages = story.pages.all().order_by('page_number')
        if not pages.exists() :
            return Response(
                {'errors' : '동화 내용이 없습니다. 페이지를 생성해야 합니다.'},
                status=status.HTTP_400_BAD_REQUEST
                                        )
        
        full_story_text = " ".join([page.content_en for page in pages])

        # AI 서버로 보낼 데이터 
        num_questions = request.data.get('num_questions', 3)

        ai_payload = {
            "story_text" : full_story_text,
            "num_questions" : num_questions
        }

        response = None

        try : 
            print(f"AI 서버로 문제 생성 요청 전송(텍스트 길이 : {(full_story_text)}")

            # 문제 생성 요청보내기
            response = requests.post(f"{AI_SERVER_URL}/story-problem", json=ai_payload)

            if response.status_code != 200 :
                print(f"문제 생성 실패 : {response.text}")
                return Response(
                    {'errors' : 'AI Question generation Failed', 'details' : response.text},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            questions_data = response.json()
            print(f"AI 문제 {len(questions_data)}개 생성 완료, DB 저장 시작..")

            # DB 저장
            created_questions = []
            with transaction.atomic() : 
                for q_item in questions_data : 
                    new_question = Question.objects.create(
                        story=story,
                        question=q_item.get('question')
                    )

                    choices_data = q_item.get('choices', [])
                    for c_item in choices_data:
                        Choice.objects.create(
                            question=new_question,
                            content=c_item.get('content'),
                            is_correct=c_item.get('is_correct')
                        )
                    created_questions.append(new_question)
            

            return Response(QuestionSerializer(created_questions, many=True).data, status=status.HTTP_201_CREATED)
        
        except requests.exceptions.RequestException as e:
            
            print(f"AI 서버 연결 오류: {e}")
            return Response({'error': 'Cannot connect to AI service.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        except Exception as e:
            
            print(f"서버 내부 오류: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
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