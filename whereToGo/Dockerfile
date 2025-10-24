# Dockerfile
# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем требования и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . /app/

# Назначаем порт
EXPOSE 8000

# КОМАНДА ЗАПУСКА: Сначала миграции, затем runserver
# runserver должен слушать 0.0.0.0, чтобы быть доступным извне контейнера
CMD python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000