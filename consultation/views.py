from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from django.contrib.auth.models import User 
import random
from django.http import JsonResponse


# 用户注册视图
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User {user.username} saved successfully!")
            return redirect('login')
        else:
            # 表单验证失败时打印错误信息
            print("Form is not valid")
            print(form.errors)  # 输出错误信息
    else:
        form = UserCreationForm()

    return render(request, 'consultation/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # 根据是否是超级管理员决定跳转
            if user.is_superuser:
                return redirect("/consultation/upload_used_car/") # 管理员跳到上传页面
            else:
                return redirect("/consultation/dashboard/")        # 普通用户跳到 dashboard
        else:
            try:
                User.objects.get(username=username)
                return render(request, 'consultation/login.html', {'error': '密码错误，请重新输入！'})
            except User.DoesNotExist:
                return render(request, 'consultation/login.html', {'error': '抱歉，您还没有注册。请点击“立即注册”进行注册！'})

    return render(request, 'consultation/login.html')



# 用户登出视图
def user_logout(request):
    logout(request)
    return redirect('register')

@login_required
def dashboard(request):
    return render(request, 'consultation/dashboard.html')

