📚 Learning Service Data Setup Guide

이 문서는 **단어 학습 서비스(Learning Service)**를 처음 실행하는 분들을 위한 데이터 적재 가이드입니다. 서비스를 정상적으로 이용하기 위해서는 **기초 단어 데이터(CSV)**를 데이터베이스에 적재해야 합니다.

🚀 시작하기 전 필수 확인 사항
Docker 컨테이너가 실행 중이어야 합니다.

Bash

docker-compose up -d
DB 마이그레이션이 완료되어 있어야 합니다.

Bash

docker-compose exec backend python manage.py migrate

📥 데이터 적재 (Import Words)
아래 명령어를 실행하면 english_words.csv 파일을 읽어 DB에 학습 데이터를 자동으로 생성합니다.

실행 명령어
터미널에서 아래 명령어를 입력하세요.

Bash

docker-compose exec backend python manage.py import_words
⚙️ 진행 과정
명령어를 실행하면 다음과 같은 작업이 순차적으로 진행됩니다.

기존 데이터 초기화: StudySet, Voca, Meaning 테이블의 기존 데이터를 모두 삭제하고 ID를 초기화합니다.

CSV 파일 로딩: backend/learning/management/english_words.csv 파일을 읽습니다.

데이터 파싱 및 저장:

레벨(Level) 및 유닛(Unit) 별로 단어장(StudySet) 생성

단어(Voca) 저장

단어의 뜻과 품사를 분리하여 의미(Meaning) 데이터 저장

✅ 성공 확인
터미널에 아래와 같은 메시지가 뜨면 적재가 완료된 것입니다.

Plaintext

기존 데이터를 삭제하고 ID를 초기화합니다...
초기화 완료. 데이터 입력을 시작합니다...
 ...Level 1 - apple 처리 중
 ...
완료! 총 OOO개의 단어 저장됨.
⚠️ 주의사항
이 명령어는 기존 학습 데이터를 모두 삭제(Reset) 합니다. 서비스 운영 중에 함부로 실행하지 않도록 주의해 주세요.

english_words.csv 파일이 backend/learning/management/ 경로에 존재하는지 확인해 주세요.