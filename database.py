from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from schemas.settings import db_settings

settings = db_settings()


class Base(DeclarativeBase): ...


DATABASE_URL = (
    f"mysql+pymysql://{settings.local_db_user}:"
    + f"{settings.local_db_password}@"
    + f"{settings.local_hostname}/{settings.local_db_name}"
)
engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
