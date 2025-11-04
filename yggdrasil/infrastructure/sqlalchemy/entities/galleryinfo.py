from datetime import date as date_
from datetime import datetime
from functools import partial
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from yggdrasil.infrastructure.sqlalchemy.association import (
    galleryinfo_artist,
    galleryinfo_character,
    galleryinfo_group,
    galleryinfo_parody,
    galleryinfo_tag,
)
from yggdrasil.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from yggdrasil.infrastructure.sqlalchemy.entities.character import CharacterSchema
from yggdrasil.infrastructure.sqlalchemy.entities.file import FileSchema
from yggdrasil.infrastructure.sqlalchemy.entities.group import GroupSchema
from yggdrasil.infrastructure.sqlalchemy.entities.language import LanguageSchema
from yggdrasil.infrastructure.sqlalchemy.entities.language_info import (
    LanguageInfoSchema,
)
from yggdrasil.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from yggdrasil.infrastructure.sqlalchemy.entities.parody import ParodySchema
from yggdrasil.infrastructure.sqlalchemy.entities.related import RelatedSchema
from yggdrasil.infrastructure.sqlalchemy.entities.scene_index import SceneIndexSchema
from yggdrasil.infrastructure.sqlalchemy.entities.tag import TagSchema
from yggdrasil.infrastructure.sqlalchemy.entities.type import TypeSchema
from yggdrasil.infrastructure.sqlalchemy.mixin import Schema

one_to_many_relationship = partial(
    relationship,
    cascade="all, delete-orphan",
    passive_deletes=True,
    lazy="selectin",
)

many_to_many_relationship = partial(
    relationship,
    passive_deletes=True,
    lazy="selectin",
)
many_to_one_relationship = partial(
    relationship,
    uselist=False,
    lazy="joined",
)


class GalleryinfoSchema(Schema):
    __tablename__ = "galleryinfo"

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    japanese_title: Mapped[Optional[str]] = mapped_column(String)
    galleryurl: Mapped[str] = mapped_column(String, nullable=False)
    video: Mapped[Optional[str]] = mapped_column(String)
    videofilename: Mapped[Optional[str]] = mapped_column(String)

    type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("type.id", ondelete="RESTRICT"), nullable=True
    )
    language_info_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("language_info.id", ondelete="RESTRICT"), nullable=True
    )
    localname_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("language_localname.id", ondelete="RESTRICT"), nullable=True
    )

    datepublished: Mapped[Optional[date_]] = mapped_column(Date, default=None)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    artists: Mapped[list[ArtistSchema]] = many_to_many_relationship(
        ArtistSchema,
        secondary=galleryinfo_artist,
    )
    characters: Mapped[list[CharacterSchema]] = many_to_many_relationship(
        CharacterSchema,
        secondary=galleryinfo_character,
    )

    groups: Mapped[list[GroupSchema]] = many_to_many_relationship(
        GroupSchema,
        secondary=galleryinfo_group,
    )
    parodys: Mapped[list[ParodySchema]] = many_to_many_relationship(
        ParodySchema,
        secondary=galleryinfo_parody,
    )
    tags: Mapped[list[TagSchema]] = many_to_many_relationship(
        TagSchema,
        secondary=galleryinfo_tag,
    )

    related: Mapped[list[RelatedSchema]] = one_to_many_relationship(RelatedSchema)

    scene_indexes: Mapped[list[SceneIndexSchema]] = one_to_many_relationship(
        SceneIndexSchema
    )
    files: Mapped[list[FileSchema]] = one_to_many_relationship(FileSchema)

    languages: Mapped[list[LanguageSchema]] = one_to_many_relationship(
        LanguageSchema,
    )

    type: Mapped[TypeSchema] = many_to_one_relationship(
        TypeSchema,
    )

    language_info: Mapped[LanguageInfoSchema] = many_to_one_relationship(
        LanguageInfoSchema,
    )

    language_localname: Mapped[LanguageLocalnameSchema] = many_to_one_relationship(
        LanguageLocalnameSchema,
    )
