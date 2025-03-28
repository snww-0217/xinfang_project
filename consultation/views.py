from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.models import User 



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
            return redirect('question_list')
        else:
            # 检查用户名是否存在
            try:
                User.objects.get(username=username)
                # 如果用户名存在但密码错误
                return render(request, 'consultation/login.html', {'error': '密码错误，请重新输入！'})
            except User.DoesNotExist:
                # 用户名不存在，显示提示让用户去注册
                return render(request, 'consultation/login.html', {'error': '抱歉，您还没有注册。请点击“立即注册”进行注册！'})

    return render(request, 'consultation/login.html')

# 用户登出视图
def user_logout(request):
    logout(request)
    return redirect('register')




# 问题列表视图
@login_required
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'consultation/question_list.html', {'questions': questions})

# 提问视图
@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # 设置提问的用户为当前登录用户
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'consultation/ask_question.html', {'form': form})

# 回复视图（管理员）
@login_required
def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)
    print(f"User is staff: {request.user.is_staff}")  # 输出当前用户是否是管理员
    if request.user.is_staff:  # 只有管理员才能回复
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.question = question
                answer.admin = request.user  # 设置回复的管理员
                answer.save()
                return redirect('question_list')
        else:
            form = AnswerForm()
        return render(request, 'consultation/answer_question.html', {'form': form, 'question': question})
    else:
        return redirect('question_list')



@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.user.is_staff:
        question.delete()
        return redirect('question_list') 
    else:
        return redirect('question_list')  
    





