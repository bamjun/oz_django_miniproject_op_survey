from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    content = models.JSONField(default=list)
    mbtidic = models.CharField(max_length=2, default='AA')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.content} - {self.mbtidic}"

class MBTIResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mbti")
    type_code = models.CharField(max_length=4, default='MBTI')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.type_code}"

class MBTIResponse(models.Model):
    mbtiresult = models.ForeignKey(
        MBTIResult, on_delete=models.CASCADE, related_name="mbti_result"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="mbti_questions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=1)  # 예: 'E', 'I', 'N', 'S', 등등

    def __str__(self):
        return f"{self.mbtiresult} - {self.question} - {self.answer}"
