import csv
import os
import re # 정규표현식 모듈 추가
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from learning.models import StudySet, Voca, Meaning

class Command(BaseCommand):
    help = 'CSV 파일에서 단어와 뜻(1:N) 데이터를 파싱하여 저장합니다.'

    def handle(self, *args, **kwargs):
        # 파일 경로 확인
        file_path = os.path.join(settings.BASE_DIR, 'learning', 'management', 'english_words.csv') 
        WORDS_PER_UNIT = 10 

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'파일을 찾을 수 없습니다: {file_path}'))
            return

        # 1. 초기화
        self.stdout.write(self.style.WARNING('기존 데이터를 삭제하고 ID를 초기화합니다...'))
        Meaning.objects.all().delete() # Meaning 부터 삭제 (Foreign Key 때문)
        Voca.objects.all().delete()
        StudySet.objects.all().delete()

        # ID 시퀀스 리셋 (PostgreSQL)
        try:
            with connection.cursor() as cursor:
                cursor.execute("ALTER SEQUENCE learning_studyset_id_seq RESTART WITH 1;")
                cursor.execute("ALTER SEQUENCE learning_voca_id_seq RESTART WITH 1;")
                cursor.execute("ALTER SEQUENCE learning_meaning_id_seq RESTART WITH 1;")
        except Exception:
            pass # SQLite 등에서는 무시

        self.stdout.write(self.style.SUCCESS('초기화 완료. 데이터 입력을 시작합니다...'))

        # 2. 파일 읽기 및 정렬
        all_rows = []
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['level'].strip().isdigit():
                    all_rows.append(row)

        all_rows.sort(key=lambda x: int(x['level']))
        
        # 3. 저장 로직
        level_counter = {} 
        total_saved = 0

        for row in all_rows:
            word_text = row['word'].strip()
            # CSV 컬럼명이 '뜻'이라고 가정합니다. 
            # 포맷: "뜻1 (품사1, Eng1), 뜻2 (품사2, Eng2)"
            meaning_raw = row['meaning'].strip() 
            level = int(row['level'])
            cefr = row['CEFR_band'].strip()

            # 유닛 번호 계산
            if level not in level_counter:
                level_counter[level] = 0
            level_counter[level] += 1
            unit_number = (level_counter[level] - 1) // WORDS_PER_UNIT + 1

            # StudySet 생성/조회
            study_set, _ = StudySet.objects.get_or_create(
                level=level, unit_number=unit_number
            )
            
            # Voca 생성 (이제 meaning 필드는 없음)
            voca = Voca.objects.create(
                level=level,
                word=word_text,
                cefr_band=cefr,
                study_set=study_set
            )

            # [핵심] 뜻 파싱 및 Meaning 객체 생성
            # 정규식 설명: 
            # 1. ([^(),]+) : 괄호나 쉼표가 아닌 문자열(=뜻)을 캡처
            # 2. \s* : 공백 무시
            # 3. \( : 여는 괄호
            # 4. ([^)]+) : 닫는 괄호 전까지의 문자열(=품사 정보)을 캡처
            # 5. \) : 닫는 괄호
            
            matches = re.findall(r'([^(),]+)\s*\(([^)]+)\)', meaning_raw)
            
            if matches:
                for content, pos in matches:
                    Meaning.objects.create(
                        voca=voca,
                        content=content.strip(),
                        part=pos.strip()
                    )
            else:
                # 괄호 패턴이 없는 경우, 전체를 그냥 뜻으로 저장 (예외 처리)
                Meaning.objects.create(
                    voca=voca,
                    content=meaning_raw,
                    part="Unknown"
                )

            total_saved += 1
            if total_saved % 100 == 0:
                print(f"  ...Level {level} - {word_text} 처리 중")

        self.stdout.write(self.style.SUCCESS(f'완료! 총 {total_saved}개의 단어 저장됨.'))