from django.urls import path
from . import views

urlpatterns = [
    # Story
    path('', views.story_list_create, name='story-list-create'), # GET, POST

    path('<int:pk>/', views.story_detail, name='story-detail'), # GET, PUT

    # path('<int:pk>/like/', views.toggle_like, name='story-like'), # POST(좋아요) -- 나중에

    path('<int:story_id>/pages/', views.story_page_list_create, name='story-page-list-create'),

    # Question
    path('<int:story_id>/questions/', views.story_question_list_create, name='story-questions'), # GET : 문제 목록, POST : 문제 생성

    # Choice
    path('questions/<int:question_id>/choices/', views.question_choice_create, name='question-choices'), # POST : 특정 문제에 선택지 추가 할 수 있도록
] 