FROM python:3.10-slim-buster

RUN pip install --no-cache-dir aiohttp \
    beautifulsoup4 \
    lxml \
    python-telegram-bot \
    telegram \
    Docker \
    asyncio \
    --upgrade pip

COPY .. /app

WORKDIR /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
