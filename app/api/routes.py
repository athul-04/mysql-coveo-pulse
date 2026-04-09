from fastapi import APIRouter,Depends
from ..database.connections import Base,engine,get_db
from typing import Annotated  
from sqlalchemy.orm import Session
from ..Models.ProductModel import Product

Base.metadata.create_all(bind=engine)

db_instance=Annotated[Session, Depends(get_db)]

router=APIRouter(
    prefix="/load",
    tags=["Data Load"]
)

@router.get("/datas")
async def get_all_data(db: db_instance):
    products = db.query(Product).all()
    return products