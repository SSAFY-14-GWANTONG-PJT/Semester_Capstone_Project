# JWT 기반의 로그인
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserStorySerializer, UserStoryAllSeializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# JWT 기반의 회원가입
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, ProfileUpdateSerializer

from .models import UserTracker
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data = request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'token' : str(refresh.access_token),
            'refreshToken' : str(refresh),
            'nickname' : user.nickname,
            'message': '회원가입 완료 및 로그인 성공! ✨'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accountDeactive(request):
    user = request.user
    refresh_token = request.data.get("refresh")

    # 1. 토큰 블랙리스트 처리 (로그아웃 로직)
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass # 이미 만료된 토큰 등 예외 처리

    # 2. 회원 탈퇴 처리 (Soft Delete)
    user.is_active = False
    user.save()

    return Response({"message": "탈퇴 및 로그아웃이 완료되었습니다."}, status=200)

# 프로필
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    
    try:
        level = user.trackers.level
    except UserTracker.DoesNotExist:
        level = 1 
    
    return Response({
        "level": level,
        "nickname": user.nickname,
        "email": user.email,
        'age': user.age,
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def profileEdit(request):
    serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "프로필이 성공적으로 업데이트되었습니다."}, status=200)
    return Response(serializer.errors, status=400)


# 내가 쓴 스토리 가져오기

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStory(request):
    user = request.user
    stories = user.stories.all()
    serializer = UserStorySerializer(stories, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllStories(request):
    user = request.user
    stories = user.stories.all()
    serializer = UserStoryAllSeializer(stories, many=True)
    return Response(serializer.data, status=200)