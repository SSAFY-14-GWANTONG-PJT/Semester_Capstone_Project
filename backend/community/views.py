from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Post, Comment, LikePost, LikeComment
from .serializers import PostSerializer, CommentSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create(request):
    # 1) 게시글 목록 조회
    if request.method == 'GET':
        qs = Post.objects.all()

        # ?status= 로 필터 (예: NORMAL)
        status_param = request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        # ?sort= 로 정렬 (예: -created_at)
        sort_param = request.query_params.get('sort', '-created_at')
        qs = qs.order_by(sort_param)

        # 간단하게 전체 반환 (나중에 pagination 붙여도 됨)
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2) 게시글 작성
    # POST /posts  (로그인 필요)
    if not request.user.is_authenticated:
        return Response(
            {'detail': '로그인이 필요합니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        # user는 request.user로 강제 세팅
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # 1) 상세 조회
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2) 수정
    if request.method == 'PUT':
        if post.user != request.user:
            return Response(
                {'detail': '본인 글만 수정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3) 삭제
    if request.method == 'DELETE':
        if post.user != request.user:
            return Response(
                {'detail': '본인 글만 삭제할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    like_obj, created = LikePost.objects.get_or_create(
        user=request.user,
        post=post,
    )

    if not created:
        # 이미 좋아요 → 취소
        like_obj.delete()
        liked = False
    else:
        liked = True

    # Post.like 카운트 필드가 있다면 여기서 동기화
    if hasattr(post, 'like'):
        post.like = LikePost.objects.filter(post=post).count()
        post.save(update_fields=['like'])

    return Response(
        {
            'liked': liked,
            'like_count': getattr(post, 'like', None),
        },
        status=status.HTTP_200_OK
    )

# 댓글목록 작성 초안만 잡아둠
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, post_id):
    """
    TODO:
    - GET: 특정 post_id 에 달린 댓글 리스트 반환
    - POST: 해당 게시글에 새 댓글 작성 (user=request.user)
    """
    # 1) post = get_object_or_404(Post, pk=post_id)

    # 2) if GET:
    #       qs = Comment.objects.filter(post=post).order_by('created_at')
    #       serializer = CommentSerializer(qs, many=True)
    #       return Response(serializer.data)

    # 3) if POST:
    #       로그인 체크 후 CommentSerializer(data=request.data)
    #       serializer.is_valid() 시 serializer.save(user=request.user, post=post)
    #       201 반환

    raise NotImplementedError("여기 로직은 네가 채워보자!")

# 댓글 수정 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_update_delete(request, comment_id):
    """
    TODO:
    - GET은 없음
    - PUT: 본인 댓글만 수정 가능
    - DELETE: 본인 댓글만 삭제 가능
    """
    # comment = get_object_or_404(Comment, pk=comment_id)
    # if request.method == 'PUT': ...
    # if request.method == 'DELETE': ...

    raise NotImplementedError("여기도 네가 구현해보면 좋아!")

# 댓글 좋아요 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_like_toggle(request, comment_id):
    """
    TODO:
    - LikeComment.objects.get_or_create(user=request.user, comment=comment)
    - created 여부에 따라 좋아요/취소 처리
    - Comment.like 카운트 있다면 동기화
    """
    # comment = get_object_or_404(Comment, pk=comment_id)
    # like_obj, created = LikeComment.objects.get_or_create(...)
    # if not created: like_obj.delete(); liked=False else liked=True
    # comment.like = LikeComment.objects.filter(comment=comment).count()
    # comment.save(update_fields=['like'])
    # return Response({...})

    raise NotImplementedError("댓글 좋아요 토글도 네가 직접 구현해보자!")
