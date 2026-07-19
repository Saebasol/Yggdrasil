from typing import Optional

from sqlalchemy import select

from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.domain.repositories.galleryinfo import GalleryinfoRepository
from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy
from yggdrasil.infrastructure.sqlalchemy.entities.deletion import (
    GalleryinfoDeletionSchema,
)
from yggdrasil.infrastructure.sqlalchemy.entities.file import FileSchema
from yggdrasil.infrastructure.sqlalchemy.entities.galleryinfo import GalleryinfoSchema
from yggdrasil.infrastructure.sqlalchemy.entities.language import LanguageSchema
from yggdrasil.infrastructure.sqlalchemy.entities.related import RelatedSchema
from yggdrasil.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.base import BaseSARepository
from yggdrasil.infrastructure.sqlalchemy.repositories.character import (
    SACharacterRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.deletion import (
    SADeletionRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.group import SAGroupRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.language_info import (
    SALanguageInfoRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.language_localname import (
    SALanguageLocalnameRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.tag import SATagRepository
from yggdrasil.infrastructure.sqlalchemy.repositories.type import SATypeRepository


class SAGalleryinfoRepository(BaseSARepository, GalleryinfoRepository):
    def __init__(
        self,
        sa: SQLAlchemy,
        type_repository: SATypeRepository,
        artist_repository: SAArtistRepository,
        language_info_repository: SALanguageInfoRepository,
        localname_repository: SALanguageLocalnameRepository,
        character_repository: SACharacterRepository,
        group_repository: SAGroupRepository,
        parody_repository: SAParodyRepository,
        tag_repository: SATagRepository,
        deletion_repository: SADeletionRepository | None = None,
    ) -> None:
        super().__init__(sa)
        self.type_repository = type_repository
        self.artist_repository = artist_repository
        self.language_info_repository = language_info_repository
        self.localname_repository = localname_repository
        self.character_repository = character_repository
        self.group_repository = group_repository
        self.parody_repository = parody_repository
        self.tag_repository = tag_repository
        self.deletion_repository = deletion_repository or SADeletionRepository(sa)

    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoSchema).where(GalleryinfoSchema.id == id)
                result = await session.execute(stmt)

                schema = result.scalar()
                if schema:
                    schema_dict = schema.to_dict()
                    return Galleryinfo.from_dict(schema_dict)
                return None

    async def get_galleryinfo_without_deleted(self, id: int) -> Optional[Galleryinfo]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoSchema).where(
                    GalleryinfoSchema.id == id,
                    ~GalleryinfoSchema.id.in_(
                        select(GalleryinfoDeletionSchema.galleryinfo_id)
                    ),
                )
                result = await session.execute(stmt)

                schema = result.scalar()
                if schema:
                    return Galleryinfo.from_dict(schema.to_dict())
                return None

    async def get_all_galleryinfo_ids(self) -> list[int]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(GalleryinfoSchema.id).order_by(GalleryinfoSchema.id)
                result = await session.execute(stmt)
                return list(result.scalars().all())

    async def get_all_galleryinfo_ids_without_deleted(self) -> list[int]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = (
                    select(GalleryinfoSchema.id)
                    .where(
                        ~GalleryinfoSchema.id.in_(
                            select(GalleryinfoDeletionSchema.galleryinfo_id)
                        )
                    )
                    .order_by(GalleryinfoSchema.id)
                )
                result = await session.execute(stmt)
                return list(result.scalars().all())

    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> int:
        async with self.sa.session_maker() as session:
            async with session.begin():
                type_schema = await self.type_repository.get_or_add_type(
                    session, galleryinfo.type
                )
                language_info_schema = (
                    await self.language_info_repository.get_or_add_language_info(
                        session, galleryinfo.language_info
                    )
                )
                language_localname_schema = (
                    await self.localname_repository.get_or_add_language_localname(
                        session, galleryinfo.language_localname
                    )
                )

                artists_schemas = (
                    await self.artist_repository.get_or_add_artists(
                        session, galleryinfo.artists
                    )
                    if galleryinfo.artists
                    else []
                )
                characters_schemas = (
                    await self.character_repository.get_or_add_characters(
                        session, galleryinfo.characters
                    )
                    if galleryinfo.characters
                    else []
                )

                groups_schemas = (
                    await self.group_repository.get_or_add_groups(
                        session, galleryinfo.groups
                    )
                    if galleryinfo.groups
                    else []
                )

                parodys_schemas = (
                    await self.parody_repository.get_or_add_parodies(
                        session, galleryinfo.parodys
                    )
                    if galleryinfo.parodys
                    else []
                )

                tags_schemas = (
                    await self.tag_repository.get_or_add_tags(session, galleryinfo.tags)
                    if galleryinfo.tags
                    else []
                )

                if galleryinfo.languages:
                    language_localnames = [
                        language.language_localname
                        for language in galleryinfo.languages
                    ]
                    language_infos = [
                        language.language_info for language in galleryinfo.languages
                    ]

                    localname_schemas = (
                        await self.localname_repository.get_or_add_language_localnames(
                            session, language_localnames
                        )
                    )
                    language_info_schemas = (
                        await self.language_info_repository.get_or_add_language_infos(
                            session, language_infos
                        )
                    )

                    localname_map = {
                        localname_schema.name: localname_schema
                        for localname_schema in localname_schemas
                    }
                    language_info_map = {
                        (
                            lang_info_schema.language,
                            lang_info_schema.language_url,
                        ): lang_info_schema
                        for lang_info_schema in language_info_schemas
                    }

                    languages_schemas: list[LanguageSchema] = []
                    for language in galleryinfo.languages:
                        language_localname_schema = localname_map[
                            language.language_localname.name
                        ]
                        language_language_info_schema = language_info_map[
                            (
                                language.language_info.language,
                                language.language_info.language_url,
                            )
                        ]
                        languages_schemas.append(
                            LanguageSchema(
                                galleryid=language.galleryid,
                                url=language.url,
                                language_info_id=language_language_info_schema.id,
                                localname_id=language_localname_schema.id,
                                language_info=language_language_info_schema,
                                language_localname=language_localname_schema,
                            )
                        )
                else:
                    languages_schemas = []

                galleryinfo_schema = GalleryinfoSchema(
                    id=galleryinfo.id,
                    type_id=type_schema.id,
                    language_info_id=language_info_schema.id,
                    localname_id=language_localname_schema.id,
                    type=type_schema,
                    language_info=language_info_schema,
                    language_localname=language_localname_schema,
                    date=galleryinfo.date,
                    title=galleryinfo.title,
                    japanese_title=galleryinfo.japanese_title,
                    galleryurl=galleryinfo.galleryurl,
                    video=galleryinfo.video,
                    videofilename=galleryinfo.videofilename,
                    datepublished=galleryinfo.datepublished,
                    blocked=galleryinfo.blocked,
                    artists=artists_schemas,
                    characters=characters_schemas,
                    groups=groups_schemas,
                    parodys=parodys_schemas,
                    tags=tags_schemas,
                    languages=languages_schemas,
                    related=[
                        RelatedSchema(related_id=related_id)
                        for related_id in galleryinfo.related
                    ],
                    scene_indexes=[
                        SceneIndexSchema(scene_index=scene_index)
                        for scene_index in galleryinfo.scene_indexes
                    ],
                    files=[
                        FileSchema.from_dict(file.to_dict())
                        for file in galleryinfo.files
                    ],
                )

                session.add(galleryinfo_schema)
                await session.commit()
                return galleryinfo_schema.id

    async def is_galleryinfo_exists(self, id: int) -> bool:
        async with self.sa.session_maker() as session:
            async with session.begin():
                stmt = select(1).where(GalleryinfoSchema.id == id)
                result = await session.execute(stmt)
                return result.scalar() is not None

    async def delete_galleryinfo(self, id: int) -> None:
        if await self.is_galleryinfo_exists(id):
            await self.deletion_repository.add_galleryinfo_deletion(id)
