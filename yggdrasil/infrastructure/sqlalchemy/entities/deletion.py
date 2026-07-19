from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from yggdrasil.infrastructure.sqlalchemy.mixin import ForeignKeySchema


class GalleryinfoDeletionSchema(ForeignKeySchema):
    __tablename__ = "galleryinfo_deletion"
    __table_args__ = (UniqueConstraint("galleryinfo_id"),)

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        init=False,
    )
