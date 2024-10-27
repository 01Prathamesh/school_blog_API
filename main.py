import logging
from fastapi import FastAPI
from school_blog.routes import router  # type: ignore

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Only show warnings and above

app = FastAPI()

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the School Blog API Created by Prathamesh Kasar"}
