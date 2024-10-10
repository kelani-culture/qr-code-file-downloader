from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
import firebase_admin  # type: ignore
import firebase_admin.app_check  # type: ignore
from fastapi import FastAPI
from schemas.settings import settings
from service.utils import decode_encoded_file_path
from firebase_admin import credentials

from routers.pdf import routers as file_converter
from routers.users import routers as user_route


setting = settings()
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize firebase on app startup...
    """
    decode_encoded_file_path(setting.service_account_key_json)
    if not firebase_admin._apps:
        cred = credentials.Certificate("service_account_key.json")
        firebase_admin.initialize_app(
            cred,
            {
                "storageBucket": "gs://qrcode-file-downloader.appspot.com",
            },
        )

    yield



app = FastAPI(lifespan=lifespan)

origins = setting.frontend_url
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def welcome_view():
    return {"info": "Welcome to pdf converter home page"}


app.include_router(user_route)
app.include_router(file_converter)
