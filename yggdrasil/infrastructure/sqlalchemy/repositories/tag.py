from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.tag import Tag
from yggdrasil.domain.repositories.tag import TagRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.tag import TagSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SATagRepository(BaseSARepository, TagRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

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

    async def get_or_add_tags(
        self, session: AsyncSession, tags: list[Tag]
    ) -> list[TagSchema]:
        if not tags:
            return []

        stmt = (
            insert(TagSchema)
            .values(
                [
                    {
                        "tag": tag.tag,
                        "url": tag.url,
                        "female": tag.female,
                        "male": tag.male,
                    }
                    for tag in tags
                ]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        tag_tuples = [(tag.tag, tag.female, tag.male) for tag in tags]
        conditions = [
            and_(
                TagSchema.tag == tag[0],
                TagSchema.female == tag[1],
                TagSchema.male == tag[2],
            )
            for tag in tag_tuples
        ]
        from sqlalchemy import or_

        result = await session.execute(select(TagSchema).where(or_(*conditions)))
        return list(result.scalars().all())

    async def get_all_tags(self) -> list[tuple[str, bool, bool]]:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(TagSchema.tag, TagSchema.male, TagSchema.female)
            )
            return [row for row in result.tuples()]
