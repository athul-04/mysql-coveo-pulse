from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..Settings.SecretSettings import settings

engine=create_engine(settings.database_url)

SessionLocal=sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()




def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


