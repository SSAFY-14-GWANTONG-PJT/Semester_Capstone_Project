from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Comment, LikeComment, LikePost
from .serializers import PostSerializer, CommentSerializer

from rest_framework.pagination import PageNumberPagination

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create(request):
    # 게시글 목록 조회
    if request.method == 'GET':
        qs = Post.objects.all()

        # ?status= 로 필터
        status_param = request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        # ?sort= 로 정렬
        sort_param = request.query_params.get('sort', '-created_at')
        qs = qs.order_by(sort_param)

        # 페이지네이션 처리 시작
        paginator = PageNumberPagination()

        page = paginator.paginate_queryset(qs, request)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            # get_paginated_response는 count, next, previous, results가 포함된 Response를 반환합니다.
            return paginator.get_paginated_response(serializer.data)
        
        # 전체 반환, 차후 pagination
        serializer = PostSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = PostSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # user는 request.user로 강제 세팅
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # 상세 조회
    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정
    if request.method == 'PUT':
        if post.user != request.user:
            return Response(
                {'detail': '본인 글만 수정할 수 있습니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
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
        # 좋아요 -> 취소
        like_obj.delete()
        liked = False
    else:
        liked = True

    like_count = LikePost.objects.filter(post=post).count()

    return Response(
        {
            'liked': liked,
            'like_count': like_count,
        },
        status=status.HTTP_200_OK
    )

# 댓글목록 작성 수정 중
@api_view(['GET', 'POST']) # get: 목록 , post : 작성(user=request.user)
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'GET':
        qs = (
            Comment.objects
            .filter(post=post)
            .select_related('user')
            .order_by('created_at')
        )
        serializer = CommentSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    serializer = CommentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 수정 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_update_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user != request.user:
        return Response(
            {"detail": "권한이 없습니다."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True,  # content만 수정 가능
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 삭제
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 좋아요 토글 (수정 중)
@api_view(['POST']) #POST /comments/{comment_id}/like
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_like_toggle(request, comment_id):
    # LikeComment 중복 방지 해야함
    comment = get_object_or_404(Comment, pk=comment_id)

    with transaction.atomic():
        like_obj, created = LikeComment.objects.get_or_create(
            user=request.user,
            comment=comment,
        )

        if created:
            liked = True
        else:
            like_obj.delete()
            liked = False

        # like count 동기화 (캐시 컬럼)
        like_count = LikeComment.objects.filter(comment=comment).count()
        comment.like = like_count
        comment.save(update_fields=['like'])

    return Response(
        {
            "comment_id": comment.id,
            "liked": liked,
            "like_count": like_count,
        },
        status=status.HTTP_200_OK
    )