from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from schemas import *
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from typing import List
from passlib.context import CryptContext
import models

app = FastAPI()

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


@app.get('/product/{id}', response_model=DisplayProduct)
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cannot find object with idx')
        return {'product not found'}
    return product


@app.post('/products', status_code=status.HTTP_201_CREATED)
def add(request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price)
    print(db)
    print(request.name)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.post('/seller', response_model= DisplaySeller)
def add_seller(request:Seller, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)

    new_Seller = models.Seller(
        username=request.name, email = request.email, password = hashed_pwd
    )
    db.add(new_Seller)
    db.commit()
    db.refresh(new_Seller)
    return request