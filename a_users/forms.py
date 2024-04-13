from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        widgets = {
            "image": forms.FileInput(),
            "displayname": forms.TextInput(attrs={"placeholder": "Add display name"}),
            "info": forms.Textarea(attrs={"rows": 3, "placeholder": "Add information"}),
            "age": forms.NumberInput(attrs={"placeholder": "Add age"}),
        }


class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]


class CustomSignupForm(SignupForm):
    age = forms.IntegerField(label="Age", widget=forms.NumberInput(attrs={'placeholder': '나이를 입력하세요.'}))
    gender = forms.ChoiceField(
        label="Gender",
        choices=(
            ('', '성별을 선택하세요.'),  # 사용자에게 보이는, 선택할 수 없는 기본 옵션
            (0, '기타'),
            (1, '남성'),
            (2, '여성'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )



    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': '사용자 이름'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': '이메일 주소'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': '비밀번호를 입력하세요.'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '비밀번호를 재입력 해주세요.'
        })




    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.age = self.cleaned_data['age']
        user.gender = self.cleaned_data['gender']
        user.save()

        return user
