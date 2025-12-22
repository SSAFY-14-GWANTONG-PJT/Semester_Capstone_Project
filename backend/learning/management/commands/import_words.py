import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection # DB 직접 제어를 위해 추가
from learning.models import StudySet, Voca

class Command(BaseCommand):
    help = '기존 데이터를 초기화(ID 리셋 포함)하고, CSV 파일의 단어들을 새로 저장합니다.'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'learning', 'management', 'english_words.csv') 
        WORDS_PER_UNIT = 10 

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'파일을 찾을 수 없습니다: {file_path}'))
            return

        # ==========================================
        # 1. 기존 데이터 삭제 & ID 리셋 (PostgreSQL 전용)
        # ==========================================
        self.stdout.write(self.style.WARNING('기존 데이터를 삭제하고 ID를 초기화합니다...'))
        
        # 데이터 삭제
        Voca.objects.all().delete()
        StudySet.objects.all().delete()

        # [핵심] 번호표 기계(Sequence)를 1번으로 강제 리셋
        # 테이블명_id_seq 규칙을 따릅니다.
        try:
            with connection.cursor() as cursor:
                cursor.execute("ALTER SEQUENCE learning_studyset_id_seq RESTART WITH 1;")
                cursor.execute("ALTER SEQUENCE learning_voca_id_seq RESTART WITH 1;")
            self.stdout.write(self.style.SUCCESS('  -> ID 카운터 리셋 완료 (1번부터 시작)'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  -> ID 리셋 실패 (SQLite 등 다른 DB일 수 있음): {e}'))

        self.stdout.write(self.style.SUCCESS('초기화 완료!'))
        self.stdout.write(self.style.SUCCESS('새로운 파일 읽기 및 레벨별 정렬 시작...'))

        # ==========================================
        # 2. 데이터 읽기 및 정렬
        # ==========================================
        all_rows = []
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['level'].strip().isdigit():
                    all_rows.append(row)

        all_rows.sort(key=lambda x: int(x['level']))
        
        # ==========================================
        # 3. 데이터 저장
        # ==========================================
        level_counter = {} 
        total_saved = 0

        for row in all_rows:
            word_text = row['word'].strip()
            meaning = row['meaning'].strip()
            level = int(row['level'])
            cefr = row['CEFR_band'].strip()

            if level not in level_counter:
                level_counter[level] = 0
            
            level_counter[level] += 1
            current_count = level_counter[level]
            
            unit_number = (current_count - 1) // WORDS_PER_UNIT + 1

            study_set, created = StudySet.objects.get_or_create(
                level=level,
                unit_number=unit_number
            )
            
            Voca.objects.create(
                level=level,
                word=word_text,
                meaning=meaning,
                cefr_band=cefr,
                study_set=study_set
            )
            total_saved += 1
            
            if total_saved % 100 == 0:
                print(f"  ...Level {level} 처리 중 (누적 {total_saved}개)")

        self.stdout.write(self.style.SUCCESS(f'작업 완료! 총 {total_saved}개의 단어가 저장되었습니다.'))