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
    meaning = models.CharField(max_length=300)
    cefr_band = models.CharField(max_length=30)
    
    def __str__(self) :
        return f"{self.word} ({self.meaning})"