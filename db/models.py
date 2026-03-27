from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class UserBase(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    role: Mapped[str] = mapped_column(String(15), default="user")

class MessageBase(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    content: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    model_label: Mapped[str | None] = mapped_column(String(10), nullable=True)
    final_label: Mapped[str | None] = mapped_column(String(10), nullable=True)
