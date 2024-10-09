from firebase_admin import credentials
import firebase_admin
cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": "qrcode-file-downloader.appspot.com",
    },
)