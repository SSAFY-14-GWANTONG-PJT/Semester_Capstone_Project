from django.urls import path
from . import views

urlpatterns = [
    # 게시글 목록 조회 + 작성
    path('posts', views.post_list_create),  # GET, POST

    # 게시글 상세 조회 / 수정 / 삭제
    path('posts/<int:post_id>', views.post_detail),  # GET, PUT, DELETE

    # 게시글 좋아요 토글
    path('posts/<int:post_id>/like', views.post_like_toggle),  # POST

    # 댓글 목록 조회 + 작성
    path('posts/<int:post_id>/comments', views.comment_list_create),  # GET, POST

    # 댓글 수정 / 삭제
    path('comments/<int:comment_id>', views.comment_update_delete),  # PUT, DELETE

    # 댓글 좋아요 토글
    path('comments/<int:comment_id>/like', views.comment_like_toggle),  # POST
]
