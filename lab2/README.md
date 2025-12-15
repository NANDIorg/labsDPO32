# Справочник товаров

Веб-приложение для управления справочником товаров и категорий.

## Стек технологий

- **Frontend:** Vue 3 + Vite + Vue Router
- **Backend:** FastAPI + SQLAlchemy
- **База данных:** PostgreSQL 15
- **Веб-сервер:** Nginx
- **Контейнеризация:** Docker + Docker Compose

## Структура проекта

```
reference-app/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models/
│       ├── schemas/
│       └── routers/
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── nginx.conf
    └── src/
        ├── App.vue
        ├── api/
        ├── router/
        └── views/
```

## Запуск

```bash
docker-compose up --build
```

После запуска:
- **http://localhost:3000** — веб-интерфейс
- **http://localhost:8000/docs** — Swagger документация API

## API эндпоинты

### Товары
| Метод | URL | Описание |
|-------|-----|----------|
| GET | /api/products/ | Список товаров |
| GET | /api/products/{id} | Получить товар |
| POST | /api/products/ | Создать товар |
| PUT | /api/products/{id} | Обновить товар |
| DELETE | /api/products/{id} | Удалить товар |

### Категории
| Метод | URL | Описание |
|-------|-----|----------|
| GET | /api/categories/ | Список категорий |
| GET | /api/categories/{id} | Получить категорию |
| POST | /api/categories/ | Создать категорию |
| PUT | /api/categories/{id} | Обновить категорию |
| DELETE | /api/categories/{id} | Удалить категорию |

## Функционал

- Просмотр, добавление, редактирование и удаление товаров
- Управление категориями товаров
- Поиск товаров по названию
- Фильтрация товаров по категории
