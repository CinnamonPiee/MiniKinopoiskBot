from database.database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, text, String, BigInteger, Text


class Users(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(str(15), nullable=False, unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("TIMEZONE('utc', now())"))


class SearchFilm(Base):
    __tablename__ = "search_film"

    name: Mapped[str] = mapped_column(String(60), nullable=False)
    janr: Mapped[str] = mapped_column(String(60), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    coast: Mapped[float] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)


class History(Base):
    __tablename__ = "history_search"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    film_id: Mapped[str] = mapped_column(ForeignKey("search_film.id"))
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("TIMEZONE('utc', now())"))
