from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

# 1. 유저 생성을 도와줄 커스텀 매니저 작성 (필수!)
# username 대신 email을 받아서 유저를 생성하도록 로직을 바꿔야 합니다.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일 주소는 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


# 2. User 모델 수정
class User(AbstractUser):
    # 기존 username 필드는 삭제 (None으로 설정하면 DB에서 사라짐)
    username = None 
    
    # email을 로그인 ID로 쓸 거니까 중복되면 안 됨 (unique=True 필수)
    email = models.EmailField(unique=True, verbose_name="이메일")
    nickname = models.CharField(max_length=20, unique=True)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 3. 장고에게 "이제부터 이메일로 로그인한다"고 알려줌
    USERNAME_FIELD = 'email'
    
    # 4. 필수로 받을 정보 목록 (USERNAME_FIELD인 email과 password는 자동으로 포함되므로 생략)
    REQUIRED_FIELDS = ['nickname', 'age']

    # 5. 위에서 만든 커스텀 매니저 연결
    objects = UserManager()

    def __str__(self):
        return self.email

class UserTracker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trackers')
    level = models.IntegerField(default=1,validators=[MaxValueValidator(10), MinValueValidator(1)])
    experience_point = models.IntegerField(default=0)
    unit_number = models.IntegerField(default=1)