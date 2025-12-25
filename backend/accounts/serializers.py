from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserTracker
from story.models import Story

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
        data['email'] = self.user.email

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
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank =True)
    class Meta:
        model = User
        fields = ['nickname', 'email', 'password']
    
    def update(self, instance, validated_data):
        # 1. 검증된 데이터에서 비밀번호를 꺼냄
        password = validated_data.pop('password', None)
        
        # 2. 이메일, 닉네임 등 일반 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # 3. 비밀번호가 존재할 때만(수정 요청이 있을 때만) 해싱하여 저장
        # 프론트에서 빈 문자열을 걸러서 보낸다면 여기서 안전하게 처리됨
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance


class UserStorySerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='author.nickname')
    thumbnail = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'title', 'like_count' ,'is_liked','summary', 'genre', 'thumbnail', 'created_at', 'status', 'user_nickname']

    def get_thumbnail(self, obj):
        first_page = obj.pages.first() 
        return first_page.image_data if first_page else None

    def get_like_count(self, obj):
        return obj.like_story.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_story.filter(user=request.user).exists()
        return False

class UpdateExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTracker
        fields = ['level', 'experience_point']

    def update(self, instance, validated_data):
        # 1. 전달받은 경험치와 레벨을 가져옵니다.
        new_exp = validated_data.get('experience_point', instance.experience_point)
        current_level = validated_data.get('level', instance.level)

        # 2. 백엔드에서 레벨업 로직을 한 번 더 검증합니다.
        # 공식: max_exp = 100 + (current_level - 1) * 20
        while True:
            max_exp = 100 + (current_level - 1) * 20
            if new_exp >= max_exp:
                if current_level >= 10: # 만렙 제한
                    new_exp = max_exp
                    break
                new_exp -= max_exp
                current_level += 1
            else:
                break
        
        instance.level = current_level
        instance.experience_point = new_exp
        instance.save()
        return instance