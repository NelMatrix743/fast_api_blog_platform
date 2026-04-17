from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils import generate_datetime
from database import Base


class User(Base):

    __tablename__: str = "users"

    # primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # user information
    username: Mapped[int] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None
    )


    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"
    

# EOSC