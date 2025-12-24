from django.urls import path
from . import views

urlpatterns = [
    # 게시글 목록 조회 + 작성
    path('posts/', views.post_list_create),  # GET, POST

    # 게시글 상세 조회 / 수정 / 삭제
    path('posts/<int:post_id>/', views.post_detail),  # GET, PUT, DELETE

    # 게시글 좋아요 모델 PostLike 아직 없기에 migrations시 에러가 발생해 주석처리 합니다
    # 게시글 좋아요 토글
    path('posts/<int:post_id>/like/', views.post_like_toggle),  # POST

    # 댓글 목록 조회 + 작성
    path('posts/<int:post_id>/comments/', views.comment_list_create),  # GET, POST

    # 댓글 수정 / 삭제
    path('comments/<int:comment_id>/', views.comment_update_delete),  # PUT, DELETE

    # 댓글 좋아요 토글
    path('comments/<int:comment_id>/like/', views.comment_like_toggle),  # POST

    # 동화 커뮤니티 동화 조회
    path('allstories/',views.getAllStories),
]
