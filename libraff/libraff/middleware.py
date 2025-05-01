import logging
from datetime import datetime, timezone

logger = logging.getLogger('middleware')

class UserActionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = datetime.now(timezone.utc)
        
        # Qeyd etmək istədiyiniz vaxtı loga daxil edirik
        log_data = {
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
            'timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),  # İstədiyiniz formatda vaxt
            'method': request.method,
            'path': request.path,
        }

        # Yalnız vaxt və istifadəçi haqqında məlumatı loglayaq
        logger.info(f"User: {log_data['user']} | Time: {log_data['timestamp']} | Method: {log_data['method']} | Path: {log_data['path']}")

        response = self.get_response(request)
        return response
