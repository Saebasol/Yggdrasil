from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.language_localname import LanguageLocalname
from yggdrasil.domain.repositories.language_localname import (
    LanguageLocalnameRepository,
)
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SALanguageLocalnameRepository(BaseSARepository, LanguageLocalnameRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

    async def get_or_add_language_localname(
        self, session: AsyncSession, localname: LanguageLocalname
    ) -> LanguageLocalnameSchema:
        result = await session.execute(
            select(LanguageLocalnameSchema).where(
                LanguageLocalnameSchema.name == localname.name
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        localname_schema = LanguageLocalnameSchema.from_dict(localname.to_dict())
        session.add(localname_schema)
        await session.flush()
        return localname_schema

    async def get_or_add_language_localnames(
        self, session: AsyncSession, localnames: list[LanguageLocalname]
    ) -> list[LanguageLocalnameSchema]:
        if not localnames:
            return []

        stmt = (
            insert(LanguageLocalnameSchema)
            .values([{"name": localname.name} for localname in localnames])
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        names = [localname.name for localname in localnames]
        result = await session.execute(
            select(LanguageLocalnameSchema).where(
                LanguageLocalnameSchema.name.in_(names)
            )
        )
        return list(result.scalars().all())
