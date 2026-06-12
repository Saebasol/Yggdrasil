from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from yggdrasil.infrastructure.sqlalchemy.mixin import Schema


class LanguageInfoSchema(Schema):
    __tablename__ = "language_info"

    language: Mapped[str] = mapped_column(String, nullable=False)
    language_url: Mapped[str] = mapped_column(String, nullable=False)

    __table_args__ = (UniqueConstraint("language", "language_url"),)
