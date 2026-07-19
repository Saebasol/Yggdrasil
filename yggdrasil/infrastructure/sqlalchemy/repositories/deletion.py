from sqlalchemy import delete, select

from yggdrasil.domain.repositories.deletion import DeletionRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.deletion import (
    GalleryinfoDeletionSchema,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SADeletionRepository(BaseSARepository, DeletionRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

    async def get_deleted_galleryinfo_ids(self) -> list[int]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoDeletionSchema.galleryinfo_id).order_by(
                    GalleryinfoDeletionSchema.galleryinfo_id
                )
                result = await session.execute(stmt)
                return list(result.scalars().all())

    async def is_galleryinfo_deleted(self, galleryinfo_id: int) -> bool:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(1).where(
                    GalleryinfoDeletionSchema.galleryinfo_id == galleryinfo_id
                )
                result = await session.execute(stmt)
                return result.scalar() is not None

    async def add_galleryinfo_deletion(self, galleryinfo_id: int) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(1).where(
                    GalleryinfoDeletionSchema.galleryinfo_id == galleryinfo_id
                )
                result = await session.execute(stmt)
                if result.scalar() is None:
                    session.add(
                        GalleryinfoDeletionSchema(galleryinfo_id=galleryinfo_id)
                    )

    async def delete_galleryinfo_deletion(self, galleryinfo_id: int) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = delete(GalleryinfoDeletionSchema).where(
                    GalleryinfoDeletionSchema.galleryinfo_id == galleryinfo_id
                )
                await session.execute(stmt)
