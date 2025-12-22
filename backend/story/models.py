from django.db import models
from django.conf import settings

# Create your models here.
class Story(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    study_set = models.ForeignKey('learning.StudySet', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')    
    title = models.CharField(max_length=200)
    summary = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=50)
    keywords = models.JSONField(default=list)

    story_level = models.IntegerField()
    like_count = models.IntegerField(default=0)

    status = models.CharField(max_length=20, default='normal') # Story를 커뮤니티에 보일지, 말지, 삭제할지를 결정하는 필드, normal = 나만 볼 수 있음, open = 다들 볼 수 있음, deleted = 나, 모두에게 안보임
    created_at = models.DateTimeField(auto_now_add=True)

class StoryPage(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    content = models.TextField() # 본문 내용
    image_data = models.TextField(null=True, blank=True) # 이미지, Base64 예정

    class Meta:
        ordering = ['page_number'] # 페이지 순 오름차순 정렬


class Question(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()

class Choice(models.Model): 
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
    


