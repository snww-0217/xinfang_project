import logging
from django.utils.timezone import localtime

# 获取日志记录器
logger = logging.getLogger('django.server')

class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取客户端 IP 地址
        ip = request.META.get('REMOTE_ADDR')
        # 获取当前时间（如果需要）
        current_time = localtime().strftime('%Y-%m-%d %H:%M:%S')
        # 将 IP 和时间记录到日志
        logger.info(f'IP: {ip} - Time: {current_time}')
        # 继续处理请求
        response = self.get_response(request)
        return response
