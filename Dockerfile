# Dockerfile
# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN pip install --no-cache-dir aiohttp beautifulsoup4 lxml python-telegram-bot telegram Docker docker-compose asyncio





# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменную окружения для Python
ENV PYTHONUNBUFFERED=1

# Команда для запуска приложения
CMD ["python", "bot.py"]
