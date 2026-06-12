from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.type import Type
from yggdrasil.domain.repositories.type import TypeRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.type import TypeSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SATypeRepository(BaseSARepository, TypeRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

    async def get_or_add_type(self, session: AsyncSession, type: Type) -> TypeSchema:
        result = await session.execute(
            select(TypeSchema).where(TypeSchema.type == type.type)
        )
        schema = result.scalars().first()

        if schema:
            return schema

        type_schema = TypeSchema.from_dict(type.to_dict())
        session.add(type_schema)
        await session.flush()
        return type_schema

    async def get_or_add_types(
        self, session: AsyncSession, types: list[Type]
    ) -> list[TypeSchema]:
        if not types:
            return []

        stmt = (
            insert(TypeSchema)
            .values([{"type": t.type} for t in types])
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        type_names = [t.type for t in types]
        result = await session.execute(
            select(TypeSchema).where(TypeSchema.type.in_(type_names))
        )
        return list(result.scalars().all())

    async def get_all_types(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(TypeSchema.type))
            return [row for row in result.scalars().all()]
