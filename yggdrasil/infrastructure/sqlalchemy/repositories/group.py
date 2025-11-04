from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.group import Group
from yggdrasil.domain.repositories.group import GroupRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.group import GroupSchema


class SAGroupRepository(GroupRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_group(
        self, session: AsyncSession, group: Group
    ) -> GroupSchema:
        result = await session.execute(
            select(GroupSchema).where(
                and_(GroupSchema.group == group.group, GroupSchema.url == group.url)
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        schema = GroupSchema.from_dict(group.to_dict())
        session.add(schema)
        await session.flush()
        return schema

    async def get_all_groups(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(GroupSchema.group))
            return [row for row in result.scalars().all()]
