from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant')
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    content = models.CharField(max_length=255)
    order_num = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.content

class Quiz(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='quizzes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='quizzes')
    chosen_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.participant.name} - {self.question.content}"