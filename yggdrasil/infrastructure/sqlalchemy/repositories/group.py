from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.group import Group
from yggdrasil.domain.repositories.group import GroupRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.group import GroupSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SAGroupRepository(BaseSARepository, GroupRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

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

    async def get_or_add_groups(
        self, session: AsyncSession, groups: list[Group]
    ) -> list[GroupSchema]:
        if not groups:
            return []

        stmt = (
            insert(GroupSchema)
            .values([{"group": group.group, "url": group.url} for group in groups])
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        group_names = [group.group for group in groups]
        group_urls = [group.url for group in groups]
        result = await session.execute(
            select(GroupSchema).where(
                and_(
                    GroupSchema.group.in_(group_names),
                    GroupSchema.url.in_(group_urls),
                )
            )
        )
        return list(result.scalars().all())

    async def get_all_groups(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(GroupSchema.group))
            return [row for row in result.scalars().all()]
