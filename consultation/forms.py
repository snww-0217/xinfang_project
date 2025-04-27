# from django import forms
# from .models import Question, Answer

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['title', 'content']

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['content']

# class UploadImageForm(forms.Form):
#     # 定义字段
#     image = forms.ImageField()



# consultation/forms.py
from django import forms
from .models import Question, Answer, ImageUpload

# 图片上传表单
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        labels = {
            'image': '上传图片',
        }

# 提问表单
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        labels = {
            'title': '问题标题',
            'content': '问题内容',
        }

# 回答表单
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '回复内容',
        }
