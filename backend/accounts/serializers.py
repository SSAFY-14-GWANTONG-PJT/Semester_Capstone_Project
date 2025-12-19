from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserTracker

# JWT를 이용한 로그인 구현 간, username이 아닌 email을 적용하기 위한 커스터 마이징
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['nickname'] = user.nickname
        return token
    
    def validate(self, attrs):
        # 2. 부모의 validate를 실행 (여기서 기본적으로 access, refresh 토큰이 생성됨)
        data = super().validate(attrs)

        # 3. Vue(프론트)에서 쓰기 편하게 이름 변경 및 데이터 추가
        # Pinia 스토어의 token 변수와 맞추기 위해 'access'를 'token'으로 변경
        data['token'] = data.pop('access') 
        # Vue에서 response.data.nickname으로 접근할 수 있도록 필드 추가
        data['nickname'] = self.user.nickname
        data['refreshToken'] = data.pop('refresh') 

        return data

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # User 모델에는 없지만 프론트에서 받을 level 정보를 정의합니다.
    level = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'nickname', 'age', 'level']
    
    def create(self, validated_data):

        level_data = validated_data.pop('level')

        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            nickname = validated_data['nickname'],
            age = validated_data['age']
        )

        UserTracker.objects.create(
            user = user,
            level = level_data
        )
        return user