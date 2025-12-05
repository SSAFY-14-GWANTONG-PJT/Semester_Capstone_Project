from django.db import models

# Create your models here.
class Story(models.Model):
    author_id = models.IntegerField() # 우선 외래키 설정 X(유저 테이블 X)
    title = models.CharField(max_length=200)
    content = models.TextField()
    genre = models.CharField(max_length=50)
    story_level = models.IntegerField()
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()

class Choice(models.Model): 
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
    


