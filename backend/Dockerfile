FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# python:3.11-slim 이라 docker 연결 부터 pip install시 터져서 
# OS 의존 패키지 설치 + pip 업그레이드 코드를 임시로 붙여 놓습니다
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# fixtures 있을 때 사용
# CMD python manage.py migrate && \
#     python manage.py loaddata 업로드할 파일 이름 && \
#     python manage.py runserver 0.0.0.0:8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]