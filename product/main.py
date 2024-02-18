from fastapi import FastAPI
from fastapi.params import Depends
from schemas import *
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from typing import List
import models

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.delete('/product/{id}')
def delete(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Product Deleted'}


@app.put('/product/{id}')
def update(id, request: Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump()
                   )
    db.commit()
    return {'product update succesfully'}


@app.get('/products')
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.get('/product/{id}', response_model=List[DisplayProduct])
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
