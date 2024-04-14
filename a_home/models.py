from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    content = models.CharField(max_length=255)
    mbtidic = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.content} - {self.mbtidic}"


class Quiz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="quizzes"
    )
    chosen_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question.content}"


class MBTIType(models.Model):
    type_code = models.CharField(max_length=4, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.type_code} - {self.description}"


class MBTIResponse(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mbti_responses"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="mbti_questions"
    )
    answer = models.CharField(max_length=1)  # 예: 'E', 'I', 'N', 'S', 등등

    def __str__(self):
        return f"{self.user.username} - {self.question} - {self.answer}"
