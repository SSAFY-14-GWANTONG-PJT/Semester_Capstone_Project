from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenBlacklistView,TokenRefreshView

urlpatterns = [
    path('login/',views.MyTokenObtainPairView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('signup/',views.signup),
    path('accountDeactive/', views.accountDeactive),
    path('profile/',views.profile),
    path('profile/edit/', views.profileEdit),
    path('profile/stories/',views.getMyStories),
    path('verify-password/', views.verify_password),
    path('update-exp/',views.updateExp)
]