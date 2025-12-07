from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # AbstractUser에 '비밀번호를 암호화하는 로직과 필드가 존재'
    # password = models.CharField() -> 사용 시, 평문으로 저장

    # AbstractUser에 'username'필드가 user_login_id와 동일한 역할 수행
    # user_login_id = models.CharField()
    nickname = models.CharField(max_length=20,unique=True)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 관리자 생성 시 추가로 입력받을 필드 목록 (TEST 편의를 위해 작성)
    REQUIRED_FIELDS = ['nickname', 'age']