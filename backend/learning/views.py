from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
import random

from .models import StudySet, Voca, Meaning
from .serializers import VocaSerializer
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


        # 단어를 꺼내서 VocaSerializer로
        vocas = study_set.vocas.all().order_by('id')

        serializer = VocaSerializer(vocas, many=True)
        
        
        return Response({
            "can_study": True,
            "current_level": tracker.level,
            "current_unit": tracker.unit_number,
            "data" : {
                "vocas" : serializer.data
            }
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
            "unit_number": tracker.unit_number,
        }, status=status.HTTP_200_OK)
        
# 온보딩 함수
class OnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        온보딩용 10문제 생성 API
        - 난이도 1, 3, 5, 7, 9 레벨의 단어를 순차적으로 배치하여 문제 생성
        - 무조건 10문제를 채워서 반환 (데이터 유효할 때 까지 재추첨)
        - 4지 선다형 (정답 1개 + 오답 3개)
        """
        # 문제 난이도 배치: 갈수록 어려워지도록 구성 (총 10문제)
        # 예: 1~2번(Lv1), 3~4번(Lv3), 5~6번(Lv5), 7~8번(Lv7), 9~10번(Lv9)
        level_sequence = [1, 1, 3, 3, 5, 5, 7, 7, 9, 9]
        problems = []
        
        # 중복 단어 출제를 방지하기 위해 사용된 단어 ID 추적
        used_voca_ids = set()

        for idx, target_level in enumerate(level_sequence):
            
            problem_created = False
            retry_limit = 50 # 무한 루프 방지용 (데이터가 충분하다면 걸릴 일 없음)
            retry_count = 0

            # 2. 유효한 문제가 생성될 때까지 반복 (Retry Logic)
            while not problem_created and retry_count < retry_limit:
                retry_count += 1
                
                # (1) 해당 레벨의 단어 중 아직 안 쓴 것 후보 추리기
                # 최적화: 뜻(content)과 품사(part)가 비어있지 않은 뜻을 가진 단어만 1차 필터링
                candidates = Voca.objects.filter(
                    level=target_level,
                    meanings__content__isnull=False,
                    meanings__part__isnull=False
                ).exclude(
                    id__in=used_voca_ids
                ).exclude(
                    meanings__part="" # 품사가 빈 문자열인 경우 제외
                )

                # 만약 해당 레벨 단어가 다 떨어졌다면? -> 전체 레벨에서 아무거나 가져오기 (Fallback)
                if not candidates.exists():
                    candidates = Voca.objects.filter(
                        meanings__content__isnull=False
                    ).exclude(
                        id__in=used_voca_ids
                    ).exclude(
                        meanings__part=""
                    )
                
                # DB가 완전히 비어있지 않은 이상 여기서 잡힘
                if not candidates.exists():
                    break 

                # (2) 후보 중 랜덤 1개 선택
                target_voca = candidates.order_by('?').first()
                
                if not target_voca:
                    continue

                # (3) 정답 보기 선정 (품사와 뜻이 제대로 있는 것만)
                correct_meaning_obj = target_voca.meanings.exclude(part="").exclude(content="").order_by('?').first()
                
                # 단어는 있는데 쓸만한 뜻 데이터가 없으면 -> 다른 단어 뽑으러 다시 루프
                if not correct_meaning_obj:
                    continue

                # (4) 오답 보기(Distractors) 3개 생성
                distractors = list(Meaning.objects.exclude(
                    voca=target_voca
                ).exclude(
                    part=""
                ).exclude(
                    content=""
                ).order_by('?')[:3])

                # 오답 보기가 3개조차 안 모이면 -> DB 문제 -> 루프 재시도
                if len(distractors) < 3:
                    continue

                # (5) 문제 조립 성공!
                options = [correct_meaning_obj] + distractors
                random.shuffle(options)

                formatted_options = []
                for opt in options:
                    formatted_options.append({
                        "id": opt.id,
                        "content": opt.content,
                        "part": opt.part,
                        "display": f"{opt.content} ({opt.part})"
                    })

                problems.append({
                    "problem_number": idx + 1,
                    "target_word": target_voca.word,
                    "options": formatted_options,
                    "correct_option_id": correct_meaning_obj.id
                })
                
                used_voca_ids.add(target_voca.id)
                problem_created = True # 루프 탈출
        
        # 10문제가 꽉 찼는지 확인
        if len(problems) < 10:
             return Response({"error": "단어 데이터가 부족하여 문제를 생성할 수 없습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "온보딩 문제가 생성되었습니다.",
            "problems": problems
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        온보딩 결과 제출 API
        - 10문제에 대한 결과 리스트([true, false...])를 받아 처리
        """
        user = request.user
        results = request.data.get('results', [])

        # 이제 10개가 확실히 보장되므로 엄격하게 체크하거나, 
        # 혹은 방어적으로 len(results)만큼만 처리해도 됩니다. (여기선 방어적으로 작성)
        if not results:
             return Response({"error": "제출된 답안이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 경험치 테이블 (10문제 기준)
        xp_table = [30, 30, 30, 50, 50, 50, 70, 70, 70, 90]
        
        total_xp = 0
        for idx, is_correct in enumerate(results):
            if idx < len(xp_table) and is_correct:
                total_xp += xp_table[idx]

        # 레벨 계산: (XP // 100) + 1
        initial_level = 1 + (total_xp // 100)
        
        # 유저 정보 업데이트
        tracker, created = UserTracker.objects.get_or_create(user=user)
        tracker.level = initial_level
        tracker.experience_point = total_xp
        tracker.unit_number = 1
        tracker.save()

        return Response({
            "message": "레벨 테스트 완료",
            "result_level": initial_level,
            "total_xp": total_xp
        }, status=status.HTTP_200_OK)