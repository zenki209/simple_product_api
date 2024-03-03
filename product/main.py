from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from schemas import *
from database import Base, engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from typing import List
from passlib.context import CryptContext
from routers import product,seller
import models

app = FastAPI(
    title="Product API",
    description="This is a sample Product API for Learning FASTAPI",
    contact={
        "Developer Name": "KHOA TRINH"
    }
)

app.include_router(product.router)
app.include_router(seller.router)

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")







