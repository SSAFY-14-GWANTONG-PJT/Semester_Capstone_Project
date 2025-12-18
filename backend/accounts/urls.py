from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('login/',views.MyTokenObtainPairView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('signup/',views.signup),
] 