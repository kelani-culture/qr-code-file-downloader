import firebase_admin  # type: ignore
from fastapi import FastAPI
from firebase_admin import credentials
from contextlib import asynccontextmanager

import firebase_admin.app_check #type: ignore

from routers.pdf import file_converter
from routers.users import routers as user_route





@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize firebase on app startup...
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("service_account_key.json")
        firebase_admin.initialize_app(cred)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def welcome_view():
    return {"info": "Welcome to pdf converter home page"}


app.include_router(file_converter)
app.include_router(user_route)
