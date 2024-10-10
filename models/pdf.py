# from sqlalchemy import DateTime, ForeignKey, String, func
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from database import Base


# class Document(Base):
#     __tablename__ = "pdf"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     original_file_name: Mapped[str] = mapped_column(String(100))
#     converted_file_name: Mapped[str] = mapped_column(String(100))

#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     file_path: Mapped[str] = mapped_column(String(200))
#     added_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
#     updated_at: Mapped[DateTime] = mapped_column(DateTime, server_onupdate=func.now())

#     user = relationship("User", back_populates="documents")
