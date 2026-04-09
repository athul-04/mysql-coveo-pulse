from ..Models import ProductModel
from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from decimal import Decimal


class ProductBase(BaseModel):
    ec_product_id: str = Field(..., max_length=50)
    ec_product_url: Optional[str] = None
    ec_product_name: Optional[str] = Field(None, max_length=255)
    ec_retail_price: Optional[Decimal] = None
    ec_discounted_price: Optional[Decimal] = None
    ec_images: Optional[List] = None
    ec_description: Optional[str] = None
    ec_brand: Optional[str] = Field(None, max_length=100)

    class Config:
        from_attributes = True



def map_product_to_document(product:ProductBase):
    return {
        "documentId": f"product://{product.ec_product_id}",
        "ec_product_id":product.ec_product_id,
        "ec_product_name": product.ec_product_name,
        "ec_product_url":product.ec_product_url,
        "ec_retail_price":product.ec_retail_price,
        "ec_discounted_price":product.ec_discounted_price,
        "ec_images":product.ec_images,
        "ec_description":product.ec_description
    }



