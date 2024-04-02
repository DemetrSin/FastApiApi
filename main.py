from typing import List

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import relationship

app = FastAPI()

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")


class CategoryModel(BaseModel):
    id: int
    name: str


class ProductModel(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: CategoryModel


class ProductCreateModel(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


class ProductUpdateModel(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


class CategoryCreateModel(BaseModel):
    name: str


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/categories/{category_id}", response_model=CategoryModel)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get("/categories/{category_id}/products", response_model=List[ProductModel])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_id == category_id).all()
    return products


@app.post("/products/", response_model=ProductModel)
def create_product(product: ProductCreateModel, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")

    category = db.query(Category).filter(Category.id == product.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return ProductModel(
        id=new_product.id,
        name=new_product.name,
        description=new_product.description,
        price=new_product.price,
        category=CategoryModel(id=category.id, name=category.name)
    )


@app.post('/categories/', response_model=CategoryModel)
def create_category(category: CategoryCreateModel, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    new_category = Category(
        name=category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.put("/products/{product_id}", response_model=ProductModel)
def update_product(product_id: int, product: ProductCreateModel, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    category = db.query(Category).filter(Category.id == product.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.category_id = product.category_id

    db.commit()
    db.refresh(existing_product)

    return existing_product


