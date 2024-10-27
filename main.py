# main.py
from fastapi import FastAPI
from school_blog.routes import router # type: ignore

app = FastAPI()

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the School Blog API Created by Prathamesh Kasar"}
