# Advertisement API

REST API для управления объявлениями, построенный на aiohttp и SQLAlchemy с асинхронной поддержкой.

## Технологии

- **aiohttp** - асинхронный веб-фреймворк
- **SQLAlchemy** - ORM с поддержкой async (asyncpg)
- **PostgreSQL** - база данных
- **Docker** - контейнеризация БД

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd adv_aiohttp
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите PostgreSQL через Docker:
```bash
docker-compose up -d
```

5. Создайте файл `.env` с настройками БД


## Запуск

### Автоматический запуск

Для удобства можно использовать скрипт `run.sh`, который автоматически запускает PostgreSQL и сервер:

```bash
# Сделайте скрипт исполняемым (только один раз)
chmod +x run.sh

# Запустите скрипт
./run.sh
```

Скрипт выполнит:
1. Запуск PostgreSQL через Docker Compose
2. Ожидание инициализации БД (3 секунды)
3. Запуск сервера на `http://localhost:8080`

### Ручной запуск

Если вы хотите запустить компоненты по отдельности:

```bash
# Запустите PostgreSQL
docker-compose up -d

# Запустите сервер
python server.py
```


## Структура проекта

```
adv_aiohttp/
├── server.py           # Основной файл сервера с API endpoints
├── models.py           # Модели БД и настройка ORM
├── errors.py           # Кастомные классы ошибок
├── client.py           # Клиент для API (пока пустой)
├── docker-compose.yml  # Конфигурация Docker для PostgreSQL
├── .env               # Переменные окружения
└── README.md          # Этот файл
```

## Модель данных

### Advertisement
- `id` (integer) - первичный ключ
- `title` (string) - название объявления (уникальное, обязательное)
- `description` (text) - описание объявления (обязательное)
- `created_at` (datetime) - время создания (автоматическое)
- `owner_id` (integer) - ID владельца (обязательное)

## Обработка ошибок

API возвращает ошибки в формате JSON:

```json
{
  "error": "Advertisement was not found"
}
```

Коды ошибок:
- `400` - Некорректный запрос (невалидный JSON или данные)
- `404` - Объявление не найдено
- `500` - Внутренняя ошибка сервера

## Разработка

Для разработки рекомендуется использовать:
- Python 3.9+
- PostgreSQL 13+
- Docker и Docker Compose