from fastapi import APIRouter, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
import models
from schemas import *
from database import get_db
from typing import List

router = APIRouter()

@router.delete('/product/{id}', tags=['Product'])
def delete(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Product Deleted'}


@router.put('/product/{id}', tags=['Product'])
def update(id, request: Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump()
                   )
    db.commit()
    return {'product update succesfully'}



@router.post('/products', status_code=status.HTTP_201_CREATED, tags=['Product'])
def add(request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price, seller_id=1)
    print(db)
    print(request.name)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@router.get('/product/{id}', response_model=DisplayProduct, tags=['Product'])
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cannot find object with idx')
        return {'product not found'}
    return product


@router.get('/products', tags=['Product'])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


