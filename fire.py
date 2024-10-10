
from firebase_admin import credentials
import firebase_admin
from schemas.settings import settings
from service.utils import decode_encoded_file_path


decode_encoded_file_path(settings().service_account_key_json)
cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": "qrcode-file-downloader.appspot.com",
    },
)