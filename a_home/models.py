from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    content = models.JSONField(default=list)
    mbtidic = models.CharField(max_length=2, default='AA')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.content} - {self.mbtidic}"

class MBTIResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mbti")
    type_code = models.CharField(max_length=4, default='MBTI')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_code} - {self.type_code}"

class MBTIResponse(MBTIResult):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="mbti_questions"
    )
    answer = models.CharField(max_length=1)  # 예: 'E', 'I', 'N', 'S', 등등

    def __str__(self):
        return f"{self.user.username} - {self.question} - {self.answer}"
