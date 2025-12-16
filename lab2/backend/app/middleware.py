import logging
from datetime import datetime
from pathlib import Path
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Настройка логирования
LOGS_DIR = Path("/app/logs")
LOGS_DIR.mkdir(exist_ok=True)

# Настройка формата логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "connections.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования IP и времени подключения пользователей"""

    async def dispatch(self, request: Request, call_next):
        # Получаем IP адрес клиента
        client_ip = request.client.host if request.client else "unknown"

        # Проверяем заголовок X-Forwarded-For (для случаев с прокси/nginx)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()

        # Получаем текущее время
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Получаем метод и путь запроса
        method = request.method
        path = request.url.path

        # Логируем подключение
        log_message = f"[{timestamp}] IP: {client_ip} | {method} {path}"
        logger.info(log_message)

        # Продолжаем обработку запроса
        response = await call_next(request)

        return response
