from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from yggdrasil.infrastructure.sqlalchemy.mixin import Schema


class GroupSchema(Schema):
    __tablename__ = "group"

    group: Mapped[str] = mapped_column(String, unique=True)
    url: Mapped[str] = mapped_column(String)
