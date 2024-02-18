from fastapi import FastAPI
from schemas import *
from database import Base, engine
import models

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post('/products')
def add(request: Product):
    return request

