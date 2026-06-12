from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from yggdrasil.infrastructure.sqlalchemy.mixin import Schema


class ParodySchema(Schema):
    __tablename__ = "parody"

    parody: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)

    __table_args__ = (UniqueConstraint("parody", "url"),)
