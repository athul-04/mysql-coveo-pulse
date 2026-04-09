from sqlalchemy import Column, String, Text, DECIMAL
from sqlalchemy.dialects.mysql import JSON
from ..database.connections import Base


class Product(Base):
    __tablename__ = "products"

    ec_product_id = Column(String(50), primary_key=True)
    ec_product_url = Column(Text, nullable=True)
    ec_product_name = Column(String(255), nullable=True)
    ec_retail_price = Column(DECIMAL(10, 2), nullable=True)
    ec_discounted_price = Column(DECIMAL(10, 2), nullable=True)
    ec_images = Column(JSON, nullable=True)
    ec_description = Column(Text, nullable=True)
    ec_brand = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Product(id={self.ec_product_id}, name={self.ec_product_name})>"