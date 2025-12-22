from django.urls import path
from . import views

urlpatterns = [
    # 프론트엔드에서 /api/learning/today/ 로 요청하게 됩니다.
    path('today/', views.TodayLearningView.as_view(), name='today_learning'),
]