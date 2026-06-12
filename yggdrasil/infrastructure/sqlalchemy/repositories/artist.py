from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from yggdrasil.domain.entities.artist import Artist
from yggdrasil.domain.repositories.artist import ArtistRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository


class SAArtistRepository(BaseSARepository, ArtistRepository):
    def __init__(self, sa: SQLAlchemy):
        super().__init__(sa)

    async def get_or_add_artist(
        self, session: AsyncSession, artist: Artist
    ) -> ArtistSchema:
        result = await session.execute(
            select(ArtistSchema).where(
                and_(
                    ArtistSchema.artist == artist.artist,
                    ArtistSchema.url == artist.url,
                )
            )
        )
        schema = result.scalars().first()

        if schema:
            return schema

        schema = ArtistSchema.from_dict(artist.to_dict())
        session.add(schema)
        await session.flush()
        return schema

    async def get_or_add_artists(
        self, session: AsyncSession, artists: list[Artist]
    ) -> list[ArtistSchema]:
        if not artists:
            return []

        stmt = (
            insert(ArtistSchema)
            .values(
                [{"artist": artist.artist, "url": artist.url} for artist in artists]
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt)

        artist_names = [artist.artist for artist in artists]
        artist_urls = [artist.url for artist in artists]
        result = await session.execute(
            select(ArtistSchema).where(
                and_(
                    ArtistSchema.artist.in_(artist_names),
                    ArtistSchema.url.in_(artist_urls),
                )
            )
        )
        return list(result.scalars().all())

    async def get_all_artists(self) -> list[str]:
        async with self.sa.session_maker() as session:
            result = await session.execute(select(ArtistSchema.artist))
            return [row for row in result.scalars().all()]
