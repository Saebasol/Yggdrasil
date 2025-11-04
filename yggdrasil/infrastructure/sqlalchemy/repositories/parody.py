from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.parody import Parody
from yggdrasil.domain.repositories.parody import ParodyRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.parody import ParodySchema


class SAParodyRepository(ParodyRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

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

    async def get_all_parodies(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(ParodySchema.parody))
            return [row for row in result.scalars().all()]
