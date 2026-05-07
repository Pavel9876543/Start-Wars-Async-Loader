from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db import Base


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)

    birth_year: Mapped[str | None] = mapped_column(String(50))
    eye_color: Mapped[str | None] = mapped_column(String(50))
    gender: Mapped[str | None] = mapped_column(String(50))
    hair_color: Mapped[str | None] = mapped_column(String(50))
    homeworld: Mapped[str | None] = mapped_column(String(255))
    mass: Mapped[str | None] = mapped_column(String(50))
    name: Mapped[str | None] = mapped_column(String(255))
    skin_color: Mapped[str | None] = mapped_column(String(50))