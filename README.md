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
- Pagination API
- Автоматическая загрузка всех персонажей
- UPSERT защита от дубликатов
- Кэширование planet requests

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
DB_PORT=5432
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

После запуска:

- все персонажи будут загружены в PostgreSQL;
- homeworld сохраняется как название планеты;
- дубликаты автоматически игнорируются;
- загрузка выполняется асинхронно.

---

# Проверка данных

## Подключение к PostgreSQL

```bash
docker exec -it project-postgres-1 psql -U postgres
```

---

## Выбор базы данных

```sql
\c starwars_db
```

---

## Просмотр данных

```sql
SELECT * FROM people;
```

---

# Особенности реализации

## Async HTTP requests

Используется:

- aiohttp
- asyncio.gather

---

## Ограничение нагрузки

Используется:

```python
asyncio.Semaphore
```

для ограничения количества одновременных запросов.

---

## Pagination API

Загрузка персонажей выполняется через pagination API:

```text
https://www.swapi.tech/api/people?page=1&limit=10
```

Это позволяет:

- загружать всех персонажей;
- не зависеть от диапазона ID;
- корректно обрабатывать пропущенные ID.

---

## Homeworld transformation

SWAPI возвращает URL планеты:

```text
https://www.swapi.tech/api/planets/1
```

Во время загрузки выполняется дополнительный запрос,
и в БД сохраняется название планеты:

```text
Tatooine
```

---

## Planet cache

Для уменьшения количества запросов используется cache планет.

Это снижает нагрузку на API и ускоряет загрузку.

---

## UPSERT защита от дубликатов

Используется PostgreSQL:

```sql
ON CONFLICT DO NOTHING
```

Это позволяет:

- избегать duplicate records;
- не загружать все ID из БД;
- повысить производительность.

---

## Fault tolerance

Реализованы:

- retries
- timeout handling
- 404 handling

---

# Автор

Гусев Павел