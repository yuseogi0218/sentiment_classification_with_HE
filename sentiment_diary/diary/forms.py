from django import forms
from .models import Diary


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary  # 사용할 모델
        fields = ['content']  # DiaryForm에서 사용할 Diary 모델의 속성
        labels = {
            'content': '내용',
        }
