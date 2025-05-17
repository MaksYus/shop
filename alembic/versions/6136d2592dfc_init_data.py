"""init data

Revision ID: 6136d2592dfc
Revises: 
Create Date: 2025-05-17 12:01:39.579066

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float


# revision identifiers, used by Alembic.
revision = '6136d2592dfc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Сначала создаем объект таблицы для категорий
    category_table = table(
        'categories',
        column('id', Integer),
        column('name', String)
    )
    
    # Вставляем категории ПЕРВЫМИ
    op.bulk_insert(category_table,
        [
            {'id': 1, 'name': 'Электроника'},
            {'id': 2, 'name': 'Одежда'},
            {'id': 3, 'name': 'Книги'}
        ]
    )
    
    # Затем создаем объект таблицы для товаров
    product_table = table(
        'products',
        column('id', Integer),
        column('name', String),
        column('description', String),
        column('price', Float),
        column('category_id', Integer)
    )
    
    # Вставляем товары ПОСЛЕ категорий
    op.bulk_insert(product_table,
        [
            {
                'name': 'Смартфон',
                'description': 'Новый флагман',
                'price': 999.99,
                'category_id': 1  # Теперь категория с ID=1 существует
            },
            {
                'name': 'Ноутбук',
                'description': 'Мощный игровой',
                'price': 1499.99,
                'category_id': 1
            },
            {
                'name': 'Футболка',
                'description': 'Хлопковая',
                'price': 19.99,
                'category_id': 2  # Категория с ID=2 существует
            }
        ]
    )


def downgrade():
    # Удаляем добавленные данные
    op.execute("DELETE FROM products WHERE name IN ('Смартфон', 'Ноутбук', 'Футболка')")
    op.execute("DELETE FROM categories WHERE name IN ('Электроника', 'Одежда', 'Книги')")