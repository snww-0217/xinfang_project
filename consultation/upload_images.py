import time, base64, os, json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
# from django.core.files.storage import FileSystemStorage
from .forms import AnswerForm
from .models import ImageUpload
from django_redis import get_redis_connection
from django.core.paginator import Paginator
ANSWER_CORRECT = settings.ANSWER_CORRECT
MAX_TRIES = getattr(settings, 'MAX_TRIES', 3)
from .redis_client import redis_client
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'consultation/upload_form.html')


# 单个image
@login_required
def verify_answer(request):
    user_id = request.session.session_key
    if not user_id:
        request.session.create()

    answer = request.POST.get('answer')
    if not answer:
        return JsonResponse({"status": "error", "message": "未提供答案"}, status=200)

    banned_until = redis_client.get(f'banned_until:{user_id}')
    if banned_until and time.time() < float(banned_until):
        return JsonResponse({
            "status": "banned",
            "banned_until": float(banned_until)
        }, status=200)

    tries = int(redis_client.get(f'answer_tries:{user_id}') or 0)

    if answer != ANSWER_CORRECT:
        tries += 1
        redis_client.set(f'answer_tries:{user_id}', tries)

        if tries >= MAX_TRIES:
            redis_client.set(f'banned_until:{user_id}', time.time() + 600)
            return JsonResponse({
                "status": "banned",
                "banned_until": time.time() + 600
            }, status=200)

        return JsonResponse({
            "status": "error",
            "remaining_attempts": MAX_TRIES - tries
        }, status=200)

    redis_client.set(f'answer_tries:{user_id}', 0)
    return JsonResponse({"status": "success"}, status=200)


# 多个image
@login_required
def upload_image(request):
    user_id = request.session.session_key
    if not user_id:
        request.session.create()

    # 检查用户是否被禁用
    banned_until = redis_client.get(f'banned_until:{user_id}')
    if banned_until and time.time() < float(banned_until):
        return JsonResponse({"error": "您已被禁止上传，10分钟后再试"}, status=403)

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        
        # 检查文件大小
        if file.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
            return JsonResponse({"error": "文件过大，无法上传"}, status=400)

        # 将文件保存到模型中
        image_upload = ImageUpload(image=file)
        image_upload.save()

        # 获取保存后的文件 URL
        file_url = image_upload.image.url

        # 返回成功响应，并指示跳转路径
        return JsonResponse({
            "message": "上传成功",
            "file_url": file_url,
            "redirect_url": "/consultation/images/"
        })

    return JsonResponse({"error": "未选择文件"}, status=400)





@login_required
def upload_images(request):
    user_id = request.session.session_key
    if not user_id:
        request.session.create()

    banned_until = redis_client.get(f'banned_until:{user_id}')
    if banned_until and time.time() < float(banned_until):
        return JsonResponse({"error": "您已被禁止上传，10分钟后再试"}, status=403)
    
    if request.method == 'POST' and request.FILES.getlist('files'):
        files = request.FILES.getlist('files')
        
        if len(files) > 3:
            return JsonResponse({"error": "一次最多上传 3 张图片"}, status=400)
        
        file_urls = []
        for file in files:
            if file.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
                return JsonResponse({"error": f"文件 {file.name} 过大，无法上传"}, status=400)
            
            # ✅ 添加 user=request.user
            image_upload = ImageUpload(image=file, user=request.user)
            image_upload.save()
            file_urls.append(image_upload.image.url)
        
        return JsonResponse({
            "message": "上传成功",
            "file_urls": file_urls,
            "redirect_url": "/consultation/images/"
        })
    
    return JsonResponse({"error": "未选择文件"}, status=400)



# 删除image操作
@login_required
def delete_image(request, image_id):
    if request.method == 'POST':
        try:
            # 获取图片对象
            image = ImageUpload.objects.get(id=image_id)

            # 调试信息
            print(f"Image user: {image.user.username}, Request user: {request.user.username}")

            # 检查当前用户是否有权限删除图片
            if request.user.is_superuser or image.user == request.user:
                image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))

                # 如果图片文件存在，删除文件
                if os.path.exists(image_path):
                    os.remove(image_path)

                # 删除数据库中的记录
                image.delete()
                return JsonResponse({"message": "图片删除成功"})

            else:
                return JsonResponse({"error": "权限不足"}, status=403)

        except ImageUpload.DoesNotExist:
            return JsonResponse({"error": "图片不存在"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"删除操作失败: {str(e)}"}, status=500)

    return JsonResponse({"error": "无效请求"}, status=400)


