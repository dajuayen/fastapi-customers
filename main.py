from fastapi import FastAPI

from config.database import engine, Base
from routers import customers

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(customers.router)


@app.get("/", tags=["Main"], description="Description Endpoint",
         name='Hello world')
async def root():
    return {"message": "Hello World"}
