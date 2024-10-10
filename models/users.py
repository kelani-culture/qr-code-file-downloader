# from typing import Optional

# from sqlalchemy import DateTime, String, func
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from database import Base

# # from .pdf import Document


# class User(Base):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     email: Mapped[str] = mapped_column(String(100), unique=True)
#     password: Mapped[str] = mapped_column(String(200))
#     created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
#     updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, onupdate=func.now())


#     documents = relationship("Document", back_populates="user")
