FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# fixtures 있을 때 사용
# CMD python manage.py migrate && \
#     python manage.py loaddata 업로드할 파일 이름 && \
#     python manage.py runserver 0.0.0.0:8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]