from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from app.models import Base
from app.database import engine, SessionLocal
from app.schemas import (
    Category, CategoryCreate,
    Product, ProductCreate,
    Order, OrderCreate,
    OrderItem
)
from app.crud import (
    get_categories, create_category, get_category,
    get_products, create_product, get_product,
    get_products_by_category, create_order, get_order, get_orders
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv("SERVER_IP", "0.0.0.0"),  # Берем IP из .env или 0.0.0.0 по умолчанию
        port=int(os.getenv("SERVER_PORT", 8000))
    )

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Категории
@app.post("/categories/", response_model=Category)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db=db, category=category)


@app.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


# Товары
@app.post("/products/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)


@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/categories/{category_id}/products/", response_model=List[Product])
def read_category_products(category_id: int, db: Session = Depends(get_db)):
    products = get_products_by_category(db, category_id=category_id)
    return products


# Заказы
@app.post("/orders/", response_model=Order)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)


@app.get("/orders/", response_model=List[Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order