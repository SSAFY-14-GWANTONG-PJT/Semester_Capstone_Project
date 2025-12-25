# JWT 기반의 로그인
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserStorySerializer, SignUpSerializer, ProfileUpdateSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# JWT 기반의 회원가입
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
            'email': user.email,
            'message': '회원가입 완료 및 로그인 성공! ✨'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

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

# 비번 확인
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_password(request):
    password = request.data.get('password')
    user = request.user
    
    if check_password(password, user.password):
        return Response({"message": "확인 완료"}, status=200)
    else:
        return Response({"message": "비밀번호가 틀립니다."}, status=400)

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
from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def getMyStories(request):
    user = request.user
    # 1. 사용자의 모든 동화를 가져오고 정렬 (최신순 등)
    stories = user.stories.all().order_by('-created_at')

    # 2. 프론트엔드에서 전체 데이터를 원하는지 확인 (?no_pagination=true)
    no_pagination = request.query_params.get('no_pagination', 'false')

    if no_pagination == 'true':
        # 전체 데이터를 한 번에 반환 (Vue에서 실시간 검색/페이지네이션 처리용)
        serializer = UserStorySerializer(stories, many=True)
        return Response(serializer.data, status=200)

    # 3. 기본값은 페이지네이션 처리 (일반적인 API 응답 방식)
    paginator = PageNumberPagination()
    # settings.py에 설정된 PAGE_SIZE(6개)를 따릅니다.
    page = paginator.paginate_queryset(stories, request)
    
    if page is not None:
        serializer = UserStorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # 예외 케이스: 페이지네이션이 적용되지 않았을 때
    serializer = UserStorySerializer(stories, many=True)
    return Response(serializer.data, status=200)

# 모든 스토리 가져오기