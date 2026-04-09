from ..Models.ProductModel import Product
from typing import List
from ..Coveo.client import push_products

async def sync_datas(products:List[Product]):
    push_products(products=products)

