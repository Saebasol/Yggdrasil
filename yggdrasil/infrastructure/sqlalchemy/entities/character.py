from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from yggdrasil.infrastructure.sqlalchemy.mixin import Schema


@dataclass
class CharacterSchema(Schema):
    __tablename__ = "character"

    character: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)

    __table_args__ = (UniqueConstraint("character", "url"),)
