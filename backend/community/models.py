from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, default='NORMAL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_like_comment")
        ]

