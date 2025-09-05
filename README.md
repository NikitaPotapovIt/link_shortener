Link Shortener - Сервис сокращения ссылок

О проекте

Link Shortener - это полнофункциональное веб-приложение для создания коротких и удобных ссылок. Сервис позволяет преобразовывать длинные URL в компактные ссылки с возможностью кастомизации и отслеживания статистики.

Что было применено:

Backend (FastAPI)

    FastAPI - современный высокопроизводительный фреймворк

    SQLAlchemy - ORM для работы с базой данных

    SQLite - легковесная база данных

    Pydantic - валидация данных и схемы

    ShortUUID - генерация уникальных коротких идентификаторов

Frontend (Tkinter)

    Tkinter - кроссплатформенный GUI фреймворк

    Requests - HTTP-запросы к API

Вспомогательные библиотеки

    Validators - проверка корректности URL

    Python-dotenv - управление переменными окружения

    Uvicorn - ASGI-сервер для FastAPI

Быстрый запуск
1. Клонирование и настройка
bash

git clone <ваш-репозиторий>
cd link_shortener/backend

2. Создание виртуального окружения
bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

3. Установка зависимостей
bash

pip install fastapi uvicorn sqlalchemy validators shortuuid python-dotenv pydantic-settings requests
# или
pip install -r requirements.txt

4. Настройка переменных окружения

Создайте файл .env в папке backend:
env

DATABASE_URL=sqlite:///./url_shortener.db
BASE_URL=http://localhost:8000
SHORT_CODE_LENGTH=6

5. Запуск сервера
bash

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8001

6. Запуск клиента
bash

cd frontend
python tkinter_app.py

Доступ к приложению

    API Сервер: http://localhost:8001

    Документация API: http://localhost:8001/docs

    Tkinter Клиент: Запускается отдельным приложением

Основные функции
Создание коротких ссылок

    Автоматическая генерация случайных кодов (6 символов)

    Возможность задания кастомных кодов (3-20 символов)

    Валидация URL перед созданием

Статистика

    Подсчет количества переходов по каждой ссылке

    Общая статистика сервиса

API Endpoints

    POST /api/shorten - создание короткой ссылки

    GET /{short_code} - перенаправление на оригинальный URL

    GET /api/info/{short_code} - информация о ссылке

    GET /api/stats - общая статистика

Публичный доступ к ссылкам

По умолчанию ссылки работают только локально. Чтобы делиться ими с другими:
1. Временное решение (Ngrok)
bash

# Установите ngrok
brew install ngrok  # Mac
# или скачайте с ngrok.com

# Запустите туннель
ngrok http 8001

# Обновите BASE_URL в .env
BASE_URL=https://ваш-ngrok-адрес.ngrok-free.app

2. Постоянное решение (Хостинг)

    Выберите хостинг: PythonAnywhere, Heroku, VPS

    Загрузите код на сервер

    Настройте базу данных (PostgreSQL для production)

    Обновите BASE_URL на ваш домен

    Настройте DNS при необходимости

3. Рекомендуемые хостинги

    PythonAnywhere - бесплатно для небольших проектов

    Heroku - требует настройки Procfile

    DigitalOcean - $5/месяц, полный контроль

Troubleshooting
Порт занят
bash

# Найдите процесс использующий порт 8000
lsof -i :8001

# Завершите процесс
kill -9 "PID - значение"

Ошибки зависимостей
bash

# Убедитесь что все пакеты установлены
pip list | grep -E "fastapi|uvicorn|sqlalchemy"

Не работает Tkinter клиент

    Проверьте что сервер запущен на порту 8001

    Убедитесь что установлен пакет requests

Примеры использования
Через API
bash

curl -X POST "http://localhost:8001/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com"}'

Через Tkinter

    Запустите tkinter_app.py

    Введите URL в поле "Введите URL"

    Опционально: Свой код ссылки

    Нажмите "Сократить"

    Скопируйте полученную ссылку
