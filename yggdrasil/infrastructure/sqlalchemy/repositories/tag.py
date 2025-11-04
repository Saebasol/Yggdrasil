from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.tag import Tag
from yggdrasil.domain.repositories.tag import TagRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.tag import TagSchema


class SATagRepository(TagRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_add_tag(self, session: AsyncSession, tag: Tag) -> TagSchema:
        result = await session.execute(
            select(TagSchema).where(
                and_(
                    TagSchema.tag == tag.tag,
                    TagSchema.url == tag.url,
                    TagSchema.female == tag.female,
                    TagSchema.male == tag.male,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        schema = TagSchema.from_dict(tag.to_dict())
        session.add(schema)
        await session.flush()
        return schema

    async def get_all_tags(self) -> list[tuple[str, bool, bool]]:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(TagSchema.tag, TagSchema.male, TagSchema.female)
            )
            return [row for row in result.tuples()]
