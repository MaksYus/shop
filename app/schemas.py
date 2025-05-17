from pydantic import BaseModel, EmailStr
from typing import List, Optional


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int
    
    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    shipping_address: str
    total_amount: float
    items: List[OrderItemCreate]


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    items: List[OrderItem]
    
    class Config:
        orm_mode = True