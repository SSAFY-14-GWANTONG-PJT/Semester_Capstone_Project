from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import StudySet
from .serializers import StudySetSerializer
from accounts.models import UserTracker

class TodayLearningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """현재 학습해야 할 단어장(StudySet) 가져오기"""
        user = request.user
        tracker, _ = UserTracker.objects.get_or_create(user=user)
        
        try:
            study_set = StudySet.objects.get(
                level=tracker.level,
                unit_number=tracker.unit_number
            )
        except StudySet.DoesNotExist:
            if StudySet.objects.filter(level=tracker.level + 1, unit_number=1).exists():
                 return Response({
                    "message": "현재 레벨 학습이 완료되었습니다. 학습 완료 버튼을 눌러 레벨업하세요!",
                    "can_study": False,
                    "need_level_up": True
                }, status=status.HTTP_200_OK)
            
            return Response({
                "message": "모든 학습 과정을 완료했습니다! 대단해요!",
                "can_study": False
            }, status=status.HTTP_200_OK)

        serializer = StudySetSerializer(study_set)
        return Response({
            "data": serializer.data,
            "can_study": True,
            "current_level": tracker.level,
            "current_unit": tracker.unit_number
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """'학습 완료' 버튼 클릭 시 호출 -> 진도 업데이트"""
        user = request.user
        tracker = get_object_or_404(UserTracker, user=user)

        current_level = tracker.level
        current_unit = tracker.unit_number
        message = ""

        # 1. 다음 유닛이 있는지 확인
        if StudySet.objects.filter(level=current_level, unit_number=current_unit + 1).exists():
            tracker.unit_number += 1
            message = "학습 완료! 다음 유닛으로 넘어갑니다."
        # 2. 다음 유닛이 없으면 다음 레벨 확인
        elif StudySet.objects.filter(level=current_level + 1, unit_number=1).exists():
            tracker.level += 1
            tracker.unit_number = 1
            message = f"축하합니다! Level {tracker.level}로 레벨업 하셨습니다!"
        else:
            return Response({"message": "모든 커리큘럼을 마치셨습니다.", "finished": True}, status=status.HTTP_200_OK)

        tracker.experience_point += 10
        tracker.save()

        return Response({
            "message": message,
            "level": tracker.level,
            "unit_number": tracker.unit_number
        }, status=status.HTTP_200_OK)