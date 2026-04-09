from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url:str
    coveo_api_key:str
    coveo_org_id:str
    coveo_batch_size:int
    coveo_source_id:str

    class Config:
        env_file = ".env"

settings=Settings()