# Приложение для ведения магазина
## Установка и запуск
### клонирование репозитория
```bash
git clone git@github.com:MaksYus/shop.git
cd shop_project
```
### Настройка переменных окружения
Создайте .env файл со следующим содержанием:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=shop_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

SERVER_IP=192.168.1.100 # Например: 192.168.1.100 или 85.123.45.67
SERVER_PORT=8000
```
### Запуск с помощью Docker
```bash
docker-compose up -d --build
```
после запуска приложение будет доступно по http://&{SERVER_IP}:&{SERVER_PORT}

## API эндпоинты
### Документация API доступна после запуска:

+ Swagger UI: http://&{SERVER_IP}:&{SERVER_PORT}/docs

+ ReDoc: http://&{SERVER_IP}:&{SERVER_PORT}/redoc

### Основные endpoint'ы:

#### Категории 

**Получение списка категорий**
``` bash
GET /categories/
```
Ответ:
```json
[
    {"name":"Электроника","id":1},
    ...
]
```

**Создание категории**  
```bash
POST /categories/

"Content-Type: application/json"
```
Тело Запроса:
```json
{
    "name" : "string"
}
```

Пример:
```bash
curl -X POST "http://localhost:8000/categories/" \
-H "Content-Type: application/json" \
-d '{"name": "Тестовая категория"}'
```

Ответ:
```json
{
    "name": "Тестовая категория",
    "id": 1
}
```

**получить категорию по ID**

```bash
GET /categories/{id}
```
Ответ:
```json
{
    "name": "Тестовая категория",
    "id": 1
}
```

#### Товары 

+ GET /products/ - список товаров

+ POST /products/ - создать товар

    ```bash
    curl -X POST "http://localhost:8000/products/" \
    -H "Content-Type: application/json" \
    -d '{"name": "Тестовый продукт",
    "description": "Описание продукта",
    "price": 123.123 ,
    "category_id": 1
    }'
    ```

+ GET /products/{id} - получить товар по ID

+ GET /categories/{id}/products/ - товары по категории

#### Заказы
+ GET /orders/ - список заказов

+ POST /orders/ - создать заказ
    ```bash
    curl -X POST "http://localhost:8000/orders/" \
    -H "Content-Type: application/json" \
    -d '{"customer_name": "Имя покупателя",
    "customer_email": "cus_email@mail.com",
    "shipping_address": "ул. пушкина 123",
    "total_amount": 123.321,
    "items": [
        {
        "product_id": 2,
        "quantity": 123,
        "price": 123.321
        }
    ]
    }'
    ```

+ GET /orders/{id} - получить заказ по ID

## Миграции базы данных
### Создание новой миграции
```bash
docker-compose exec web alembic revision --autogenerate -m "Описание изменений"
```
### Применение миграций
```bash
docker-compose exec web alembic upgrade head
```
### Откат миграции
```bash
docker-compose exec web alembic downgrade -1
```


## Тестирование:

АТ располагается в ./tests . Для запуска тестирования нужно переименовать .env в .env.dev и
.env.test в .env (после завершения тестирования вернуть обратон)

Поднять приложение используя следующие команды:
```bash
docker-compose build --no-cache && docker-compose up -d
```
После того, как приложение подниматся, можно проводить тестирование.