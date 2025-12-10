from django.contrib import admin
from .models import Story, StoryPage, Question, Choice

# Register your models here.
admin.site.register(Story)
admin.site.register(StoryPage)
admin.site.register(Question)
admin.site.register(Choice)