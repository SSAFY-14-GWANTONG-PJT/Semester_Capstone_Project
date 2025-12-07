from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer


@api_view(['POST']) 
def login(request):
    
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'nickname': user.nickname,
                'message': '로그인 성공!'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': '아이디/비번 불일치'}, status=status.HTTP_401_UNAUTHORIZED)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)