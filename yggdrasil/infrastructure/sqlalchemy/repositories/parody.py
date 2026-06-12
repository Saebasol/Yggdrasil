from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.parody import Parody
from yggdrasil.domain.repositories.parody import ParodyRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.parody import ParodySchema
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SAParodyRepository(BaseSARepository, ParodyRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

    async def get_or_add_parody(
        self, session: AsyncSession, parody: Parody
    ) -> ParodySchema:
        result = await session.execute(
            select(ParodySchema).where(
                and_(
                    ParodySchema.parody == parody.parody,
                    ParodySchema.url == parody.url,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        schema = ParodySchema.from_dict(parody.to_dict())
        session.add(schema)
        await session.flush()
        return schema

    async def get_or_add_parodies(
        self, session: AsyncSession, parodies: list[Parody]
    ) -> list[ParodySchema]:
        if not parodies:
            return []

        stmt = (
            insert(ParodySchema)
            .values(
                [{"parody": parody.parody, "url": parody.url} for parody in parodies]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        parody_names = [parody.parody for parody in parodies]
        parody_urls = [parody.url for parody in parodies]
        result = await session.execute(
            select(ParodySchema).where(
                and_(
                    ParodySchema.parody.in_(parody_names),
                    ParodySchema.url.in_(parody_urls),
                )
            )
        )
        return list(result.scalars().all())

    async def get_all_parodies(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(ParodySchema.parody))
            return [row for row in result.scalars().all()]
