from rest_framework import serializers
from .models import Post, Comment, LikePost, LikeComment
from story.models import Story

class PostSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    user_email = serializers.ReadOnlyField(source='user.email')
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user']
    
    def get_like_count(self, obj):
        # LikePost 모델에서 현재 게시물(obj)의 좋아요 총 개수를 구합니다.
        return LikePost.objects.filter(post=obj).count()

    def get_is_liked(self, obj):
    # 1. context에서 request를 안전하게 가져옵니다.
        request = self.context.get('request')
        
        # 2. request가 없거나 유저 정보가 없으면 False 반환
        if not request or not hasattr(request, 'user'):
            return False
            
        user = request.user
        
        # 3. 로그인한 유저인 경우에만 좋아요 여부 확인
        if user.is_authenticated:
            # LikePost 모델의 이름을 확인하세요 (예: LikePost 또는 PostLike)
            return LikePost.objects.filter(post=obj, user=user).exists()
        
        return False
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'post']

    def get_like_count(self, obj):
        return LikeComment.objects.filter(comment=obj).count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LikeComment.objects.filter(comment=obj, user=request.user).exists()
        return False


class UserStoryAllSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='author.nickname')
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    # 썸네일 필드
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'
    
    def get_like_count(self, obj):
        return obj.like_story.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.like_story.filter(user=user).exists()
        return False
    
    def get_thumbnail(self, obj):
        first_page = obj.pages.first()
        if first_page:
            return first_page.image_data
        return None