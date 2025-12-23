from django.urls import path
from .views import TodayLearningView, OnboardingView

urlpatterns = [
    path('today/', TodayLearningView.as_view(), name='today_learning'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
]