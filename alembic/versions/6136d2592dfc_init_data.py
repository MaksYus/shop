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

     # Создаем таблицу categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

    # Создаем таблицу products
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

    # Создаем таблицу orders
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('customer_name', sa.String(100), nullable=False),
        sa.Column('customer_email', sa.String(100)),
        sa.Column('total_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    # Создаем таблицу order_items
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False)
    )

    # Создаем индексы
    op.create_index(op.f('ix_products_category_id'), 'products', ['category_id'])
    op.create_index(op.f('ix_order_items_order_id'), 'order_items', ['order_id'])
    op.create_index(op.f('ix_order_items_product_id'), 'order_items', ['product_id'])


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
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('categories')