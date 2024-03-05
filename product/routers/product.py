from fastapi import APIRouter, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
import models
from schemas import *
from database import get_db
from typing import List
from routers import login

router = APIRouter(
    tags=['product'],
    prefix="/product"
)

@router.delete('/{id}')
def delete(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Product Deleted'}


@router.put('/{id}')
def update(id, request: Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump()
                   )
    db.commit()
    return {'product update succesfully'}



@router.post('/', status_code=status.HTTP_201_CREATED)
def add(request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price, seller_id=1)
    print(db)
    print(request.name)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@router.get('/{id}', response_model=DisplayProduct)
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cannot find object with idx')
        return {'product not found'}
    return product


@router.get('/')
def products(db: Session = Depends(get_db), current_login_user: Seller = Depends(login.get_current_user)):
    products = db.query(models.Product).all()
    return products


