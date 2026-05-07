# README.md

# Star Wars Async Loader

Асинхронная загрузка персонажей Star Wars из SWAPI в PostgreSQL.

## Stack

- Python 3.10+
- asyncio
- aiohttp
- SQLAlchemy Async
- PostgreSQL
- Docker
- Alembic

---

# Возможности

- Асинхронная загрузка данных из API
- Конкурентные HTTP-запросы
- Ограничение количества одновременных запросов
- Обработка timeout и network errors
- Обработка 404 ошибок
- Async PostgreSQL
- Dockerized PostgreSQL
- Alembic migrations

---

# Структура проекта

```text
Start-Wars-Async-Loader/
│
├── app/
│   ├── config.py
│   ├── db.py
│   ├── loader.py
│   ├── main.py
│   ├── models.py
│   └── swapi.py
│
├── migrations/
│
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

# Установка

## 1. Клонировать проект

```bash
git clone https://github.com/Pavel9876543/Start-Wars-Async-Loader
cd Start-Wars-Async-Loader
```
---

## 2. Создать виртуальное окружение

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

# Настройка .env

Создать файл `.env` по шаблону `.env.example`

Пример:
```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=starwars_db
DB_USER=postgres
DB_PASSWORD=postgres
```

---

# Запуск PostgreSQL

## Запуск контейнера

```bash
docker compose up -d
```

---

## Проверка контейнера

```bash
docker ps
```

---

# Миграции

## Создать migration

```bash
alembic revision --autogenerate -m "create people table"
```

---

## Применить migrations

```bash
alembic upgrade head
```

---

# Запуск проекта

```bash
python -m app.main
```

---

# Результат

После запуска все персонажи будут загружены в PostgreSQL.

---

# Проверка данных

## Подключение к PostgreSQL

```bash
docker exec -it project-postgres-1 psql -U postgres
```

---

## Выбор базы данных

```sql
\c <DB_NAME>
```

---

## Просмотр данных

```sql
SELECT * FROM people LIMIT 10;
```

---

# Особенности реализации

## Async HTTP requests

Используется:

* aiohttp
* asyncio.gather

---

## Ограничение нагрузки

Используется:

```python
asyncio.Semaphore
```

для ограничения количества одновременных запросов.

---

## Fault tolerance

Реализованы:

* retries
* timeout handling
* 404 handling

---

# Автор

Гусев Павел
