from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.character import Character
from yggdrasil.domain.repositories.character import CharacterRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.character import CharacterSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SACharacterRepository(BaseSARepository, CharacterRepository):
    def __init__(self, sa: SQLAlchemy) -> None:
        super().__init__(sa)

    async def get_or_add_character(
        self, session: AsyncSession, character: Character
    ) -> CharacterSchema:
        result = await session.execute(
            select(CharacterSchema).where(
                and_(
                    CharacterSchema.character == character.character,
                    CharacterSchema.url == character.url,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        schema = CharacterSchema.from_dict(character.to_dict())
        session.add(schema)
        await session.flush()
        return schema

    async def get_or_add_characters(
        self, session: AsyncSession, characters: list[Character]
    ) -> list[CharacterSchema]:
        if not characters:
            return []

        stmt = (
            insert(CharacterSchema)
            .values(
                [
                    {"character": character.character, "url": character.url}
                    for character in characters
                ]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        character_names = [character.character for character in characters]
        character_urls = [character.url for character in characters]
        result = await session.execute(
            select(CharacterSchema).where(
                and_(
                    CharacterSchema.character.in_(character_names),
                    CharacterSchema.url.in_(character_urls),
                )
            )
        )
        return list(result.scalars().all())

    async def get_all_characters(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(CharacterSchema.character))
            return [row for row in result.scalars().all()]
