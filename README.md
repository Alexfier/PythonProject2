# LSM-system_drf - Django REST Framework

## Описание проекта
Веб-приложение на Django REST Framework с использованием:
- PostgreSQL 16.0 - основная база данных
- Redis 7.0 - брокер сообщений и кэширование
- Celery - асинхронные задачи
- Celery Beat - периодические задачи

## 🛠 Требования
- Docker 20.10+
- Docker Compose 1.29+
- Файл `.env` с конфигурацией

## 🚀 Запуск проекта

### 1. Настройка окружения
Создайте `.env` файл в корне проекта:
```env
# PostgreSQL
NAME=lsm_drf
USER=postgres
PASSWORD=your_secure_password

# Redis
REDIS_URL=redis://redis:6379/0

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 2. Запуск системы
В терминале выполните команду:
```
docker-compose up -d --build
```
После выполнения этой команды будут собраны образы, запустятся сервисы, будут применены миграции, запустится сервер.

## Проверка работоспособности
Для проверки основных сервисов нужно выполнить команды:
```
#Проверка статуса всех контейнеров
docker-compose ps
```

