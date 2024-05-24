# main.py
from sqlmodel import SQLModel, create_engine
import uvicorn
from fastapi import FastAPI
from app import routes

from contextlib import asynccontextmanager

def initialize():
    """ Initializes the database with all models if the table(s) do not exist. """
    from app import tables
    print('database.py: Initializing:', tables.__name__)
    SQLModel.metadata.create_all(engine)

def dispose():
    engine.dispose()

def get_url():
    # Replace with your actual database URL
    return "mysql+mysqlconnector://root:admin123@127.0.0.1/netflix"

# Create the engine globally
engine = create_engine(get_url())



@asynccontextmanager
async def lifespan(api_app: FastAPI):
    print("initialisse")
    initialize()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=routes.router, tags=['movies'])

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        dispose()
