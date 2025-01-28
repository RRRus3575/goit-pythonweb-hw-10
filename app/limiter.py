from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from slowapi.middleware import SlowAPIMiddleware

# Создаем лимитер, который считает запросы по IP-адресу
limiter = Limiter(key_func=get_remote_address)

# Функция обработки ошибок лимита
@limiter.request_filter
def exempt_health_checks(request: Request):
    """Исключаем системные проверки из лимитирования запросов"""
    return request.url.path == "/health"

# Middleware для лимитирования
def add_rate_limit_middleware(app):
    app.add_middleware(SlowAPIMiddleware)
