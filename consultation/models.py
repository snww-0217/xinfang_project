from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=255)  # 问题标题
    content = models.TextField()  # 问题内容
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 提问的用户
    created_at = models.DateTimeField(auto_now_add=True)  # 提问时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)  # 关联的问题
    content = models.TextField()  # 回复内容
    admin = models.ForeignKey(User, on_delete=models.CASCADE)  # 回复的管理员
    created_at = models.DateTimeField(auto_now_add=True)  # 回复时间

    def __str__(self):
        return f"Answer to {self.question.title}"


class ImageUpload(models.Model):
    # 文件字段，使用 Django 的 ImageField 来处理图片
    image = models.ImageField(upload_to='images/', verbose_name="上传的图片")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="上传者")
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"
