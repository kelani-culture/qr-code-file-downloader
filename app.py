from fastapi import FastAPI

from routers.pdf import file_converter

app = FastAPI()


@app.get("/")
def welcome_view():
    return {"info": "Welcome to pdf converter home page"}


app.include_router(file_converter)
