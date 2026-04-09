from fastapi import APIRouter,Depends
from ..database.connections import Base,engine,get_db
from typing import Annotated  
from sqlalchemy.orm import Session
from ..Models.ProductModel import Product
from ..pipeline.sync import sync_datas


Base.metadata.create_all(bind=engine)

db_instance=Annotated[Session, Depends(get_db)]

router=APIRouter(
    prefix="/load",
    tags=["Data Load"]
)

@router.get("/datas")
async def get_all_data(db: db_instance):
    products = db.query(Product).limit(5).all()
    return products


@router.post("/data-pulse")
async def push_all_data(db:db_instance):
    products=db.query(Product).all()
    await sync_datas(products=products)
