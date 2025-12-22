import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from learning.models import StudySet, Voca

class Command(BaseCommand):
    help = 'CSV 파일에서 단어 데이터를 읽어와 10개 단위로 Unit을 나누어 저장합니다.'

    def handle(self, *args, **kwargs):
        # 1. 파일 경로 설정
        file_path = os.path.join(settings.BASE_DIR, 'english_words.csv') 
        
        # [핵심 설정] 한 Unit당 단어 수 = 10개
        WORDS_PER_UNIT = 10 
        
        # 레벨별로 단어 개수를 카운트하기 위한 딕셔너리
        # 예: { 3: 5, 4: 12 ... } -> 레벨 3은 5번째 단어, 레벨 4는 12번째 단어 처리 중
        level_counter = {}

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'파일을 찾을 수 없습니다: {file_path}'))
            return

        self.stdout.write(self.style.SUCCESS('데이터 입력을 시작합니다... (10단어/1Unit)'))

        # 기존 데이터가 꼬일 수 있으므로, 깔끔하게 지우고 시작할지 선택 (필요시 주석 해제)
        # Voca.objects.all().delete()
        # StudySet.objects.all().delete()

        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            total_created_count = 0
            
            for row in reader:
                # 1. CSV 데이터 파싱
                word_text = row['word'].strip()
                meaning = row['meaning'].strip()
                try:
                    level = int(row['level'])
                except ValueError:
                    continue # 레벨이 숫자가 아니면 건너뜀
                cefr = row['CEFR_band'].strip()

                # 2. 레벨별 카운트 증가 및 유닛 번호 계산
                if level not in level_counter:
                    level_counter[level] = 0
                
                level_counter[level] += 1
                current_count = level_counter[level]
                
                # [핵심 로직]
                # (1~10번째 -> unit 1), (11~20번째 -> unit 2) ...
                unit_number = (current_count - 1) // WORDS_PER_UNIT + 1

                # 3. StudySet 가져오기 (없으면 생성)
                # 레벨 3, 유닛 1인 세트가 이미 있으면 가져오고, 없으면 만듦
                study_set, created = StudySet.objects.get_or_create(
                    level=level,
                    unit_number=unit_number
                )
                
                # 4. 단어(Voca) 저장
                Voca.objects.create(
                    level=level, # 단어 자체에도 레벨 정보 저장 (필요시)
                    word=word_text,
                    meaning=meaning,
                    cefr_band=cefr,
                    study_set=study_set
                )
                
                total_created_count += 1
                
                # 진행 상황 로그 (선택 사항)
                if total_created_count % 100 == 0:
                     print(f"L{level}-U{unit_number}에 '{word_text}' 저장 중... (총 {total_created_count}개)")

        self.stdout.write(self.style.SUCCESS(f'완료! 총 {total_created_count}개의 단어가 저장되었습니다.'))