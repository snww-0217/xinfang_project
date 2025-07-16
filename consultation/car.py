from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import JsonResponse
from .models import UsedCar
from django.core import serializers


@login_required
@user_passes_test(lambda u: u.is_superuser)  # 只有超级管理员能访问
def upload_used_car(request):
    if request.method == 'GET':
        # GET 请求：返回 HTML 表单页面
        return render(request, 'consultation/upload_used_car.html')
    
    elif request.method == 'POST':
        # POST 请求：处理表单数据
        try:
            brand = request.POST.get('brand')
            model = request.POST.get('model')
            production_year = request.POST.get('production_year')
            insurance_status = request.POST.get('insurance_status')
            usage_years = request.POST.get('usage_years')
            major_accident = request.POST.get('major_accident') == 'true'  # 前端传 'true'/'false'
            image = request.FILES.get('image')

            # 简单校验
            if not all([brand, model, production_year, insurance_status, usage_years, image]):
                return JsonResponse({'status': 'error', 'message': '缺少必要参数'})

            # 保存到数据库
            car = UsedCar.objects.create(
                brand=brand,
                model=model,
                production_year=int(production_year),
                insurance_status=insurance_status,
                usage_years=int(usage_years),
                major_accident=major_accident,
                image=image
            )
            return JsonResponse({'status': 'success', 'message': '上传成功', 'car_id': car.id})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'服务器错误: {str(e)}'})

@login_required
def car_list(request):
    cars = UsedCar.objects.all().order_by('-created_at')
    # 返回 json
    data = []
    for car in cars:
        data.append({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'production_year': car.production_year,
            'insurance_status': car.insurance_status,
            'usage_years': car.usage_years,
            'major_accident': car.major_accident,
            'image_url': car.image.url if car.image else ''
        })
    return JsonResponse({'status': 'success', 'cars': data}, content_type='application/json')


@login_required
def car_list_page(request):
    return render(request, 'consultation/car_list.html')
