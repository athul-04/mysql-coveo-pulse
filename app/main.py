from fastapi import FastAPI,status


app=FastAPI()

@app.get("/healthy",status_code=status.HTTP_200_OK)
async def get_server_status():
    return {"message":"Server is in healthy state"}