from sqlalchemy.orm import Session
from app.models import Product, Category, Order, OrderItem


# CRUD для категорий
def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# CRUD для товаров
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products_by_category(db: Session, category_id: int):
    return db.query(Product).filter(Product.category_id == category_id).all()


# CRUD для заказов
def create_order(db: Session, order):
    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        shipping_address=order.shipping_address,
        total_amount=order.total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()