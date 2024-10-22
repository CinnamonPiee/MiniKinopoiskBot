from sqlalchemy import ForeignKey, text, String, BigInteger, Text, DateTime, Boolean
from sqlalchemy_utils import URLType

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.databases import Base

from datetime import datetime


class User(Base):
    __tablename__ = "users_user"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    last_login: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"))
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False)
    username: Mapped[str] = mapped_column(String(150), nullable=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String(254), nullable=True, unique=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_joined: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"))
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True, unique=True)

    history_film: Mapped[list["HistoryFilm"]] = relationship(
        "HistoryFilm",
        cascade="all, delete",
        back_populates="user"
    )
    history_serial: Mapped[list["HistorySerial"]] = relationship(
        "HistorySerial",
        cascade="all, delete",
        back_populates="user"
    )


class SearchFilm(Base):
    __tablename__ = "films_serials_searchfilm"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    janr: Mapped[str] = mapped_column(String(60), nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    movie_length: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    age_rating: Mapped[int] = mapped_column(nullable=True)
    picture: Mapped[str] = mapped_column(URLType, nullable=True)

    history: Mapped[list["HistoryFilm"]] = relationship(
        "HistoryFilm",
        cascade="all, delete",
        back_populates="film"
    )


class SearchSerial(Base):
    __tablename__ = "films_serials_searchserial"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    janr: Mapped[str] = mapped_column(String(60), nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    release_year: Mapped[str] = mapped_column(String(60), nullable=True)
    series_length: Mapped[str] = mapped_column(String(10), nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    age_rating: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    picture: Mapped[str] = mapped_column(URLType, nullable=True)

    history: Mapped[list["HistorySerial"]] = relationship(
        "HistorySerial",
        cascade="all, delete",
        back_populates="serial"
    )


class HistoryFilm(Base):
    __tablename__ = "history_historyfilm"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users_user.id"))
    film_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("films_serials_searchfilm.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["User"] = relationship("User", back_populates="history_film")
    film: Mapped["SearchFilm"] = relationship("SearchFilm", back_populates="history")


class HistorySerial(Base):
    __tablename__ = "history_historyserial"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users_user.id"))
    serial_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("films_serials_searchserial.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["User"] = relationship("User", back_populates="history_serial")
    serial: Mapped["SearchSerial"] = relationship("SearchSerial", back_populates="history")
