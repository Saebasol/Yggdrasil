from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from yggdrasil.infrastructure.sqlalchemy.mixin import ForeignKeySchema


class RelatedSchema(ForeignKeySchema):
    __tablename__ = "related"

    related_id: Mapped[int] = mapped_column(Integer)
