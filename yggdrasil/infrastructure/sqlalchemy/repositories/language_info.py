from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.language_info import LanguageInfo
from yggdrasil.domain.repositories.language_info import LanguageInfoRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SALanguageInfoRepository(BaseSARepository, LanguageInfoRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

    async def get_or_add_language_info(
        self, session: AsyncSession, language_info: LanguageInfo
    ) -> LanguageInfoSchema:
        result = await session.execute(
            select(LanguageInfoSchema).where(
                and_(
                    LanguageInfoSchema.language == language_info.language,
                    LanguageInfoSchema.language_url == language_info.language_url,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        language_info_schema = LanguageInfoSchema(
            language=language_info.language,
            language_url=language_info.language_url,
        )
        session.add(language_info_schema)
        await session.flush()
        return language_info_schema

    async def get_or_add_language_infos(
        self, session: AsyncSession, language_infos: list[LanguageInfo]
    ) -> list[LanguageInfoSchema]:
        if not language_infos:
            return []

        stmt = (
            insert(LanguageInfoSchema)
            .values(
                [
                    {
                        "language": lang_info.language,
                        "language_url": lang_info.language_url,
                    }
                    for lang_info in language_infos
                ]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        lang_info_tuples = [
            (lang_info.language, lang_info.language_url) for lang_info in language_infos
        ]
        conditions = [
            and_(
                LanguageInfoSchema.language == lang_info[0],
                LanguageInfoSchema.language_url == lang_info[1],
            )
            for lang_info in lang_info_tuples
        ]
        from sqlalchemy import or_

        result = await session.execute(
            select(LanguageInfoSchema).where(or_(*conditions))
        )
        return list(result.scalars().all())

    async def get_all_language_infos(self) -> list[str]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(LanguageInfoSchema.language)
                result = await session.execute(stmt)
                return [schema for schema in result.scalars().all()]
