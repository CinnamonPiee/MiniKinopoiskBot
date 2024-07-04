from datetime import datetime
from database.databases import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text, String, BigInteger, Text, DateTime


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text("TIMEZONE('utc', now())"))

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
    __tablename__ = "search_film"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    janr: Mapped[str] = mapped_column(String(60), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    box_office: Mapped[float] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)
    rating: Mapped[float] = mapped_column(nullable=False)

    history: Mapped[list["HistoryFilm"]] = relationship(
        "HistoryFilm",
        cascade="all, delete",
        back_populates="film"
        )


class SearchSerial(Base):
    __tablename__ = "search_serial"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    janr: Mapped[str] = mapped_column(String(60), nullable=False)
    release_year: Mapped[str] = mapped_column(String(60), nullable=False)
    series_length: Mapped[str] = mapped_column(String(10), nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)
    rating: Mapped[float] = mapped_column(nullable=False)

    history: Mapped[list["HistorySerial"]] = relationship(
        "HistorySerial",
        cascade="all, delete",
        back_populates="serial")


class HistoryFilm(Base):
    __tablename__ = "history_search_film"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    film_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("search_film.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["Users"] = relationship("Users", back_populates="history_film")
    film: Mapped["SearchFilm"] = relationship("SearchFilm", back_populates="history")


class HistorySerial(Base):
    __tablename__ = "history_search_serial"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    serial_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("search_serial.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["Users"] = relationship("Users", back_populates="history_serial")
    serial: Mapped["SearchSerial"] = relationship("SearchSerial", back_populates="history")
