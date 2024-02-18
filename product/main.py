from fastapi import FastAPI
from fastapi.params import Depends
from schemas import *
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/products')
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product')
def product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product



@app.post('/products')
def add(request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price)
    print(db)
    print(request.name)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request
