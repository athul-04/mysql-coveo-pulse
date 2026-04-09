from fastapi import FastAPI,status
from api import routes

app=FastAPI()



@app.get("/healthy",status_code=status.HTTP_200_OK)
async def get_server_status():
    return {"message":"Server is in healthy state"}

app.include_router(routes.router)




