from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = (
        (0, '기타'),
        (1, '남성'),
        (2, '여성'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    age = models.IntegerField(default=0)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.user.username
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.svg')

        return avatar

