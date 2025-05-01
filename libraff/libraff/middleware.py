import logging
from datetime import datetime, timezone
from django.http import HttpResponseForbidden
from django.conf import settings

logger = logging.getLogger('middleware')

class UserActionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = datetime.now(timezone.utc)
        response = self.get_response(request)
        duration = datetime.now(timezone.utc) - start_time
        log_data = {
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration': f"{duration:.2f}s",
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }

        logger.info(
            f"User: {log_data['user']} | Method: {log_data['method']} | Path: {log_data['path']} | "
            f"Status: {log_data['status_code']} | Duration: {log_data['duration']} | "
            f"IP: {log_data['ip']} | User Agent: {log_data['user_agent']}"
        )

        return response 