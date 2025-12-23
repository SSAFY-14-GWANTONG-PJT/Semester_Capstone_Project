from django.db import models
    
class StudySet(models.Model):
    level = models.IntegerField()
    unit_number = models.IntegerField()
    
    def __str__(self):
        return f"Level {self.level} - Unit {self.unit_number}"
    
class Voca(models.Model):
    level = models.IntegerField()
    word = models.CharField(max_length=50)
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE, related_name='vocas')
    cefr_band = models.CharField(max_length=30)
    
    def __str__(self) :
        return f"{self.word} ({self.meaning})"
    
# Meaning을 둬서 한 영단어 당 매칭되는 여러 해석 뜻과 해당 뜻의 품사를 표현하는 1 : N 관계를 완성합니다
class Meaning(models.Model):
    voca = models.ForeignKey(Voca, on_delete=models.CASCADE, related_name='meanings')
    content = models.CharField(max_length=100) # 뜻
    part = models.CharField(max_length=50) # 품사 
    
    def __str__(self):
        return f"{self.content} ({self.part_of_speech})"