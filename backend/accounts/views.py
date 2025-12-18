# JWT 기반의 로그인
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# JWT 기반의 회원가입
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer

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