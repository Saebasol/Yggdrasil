from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from yggdrasil.domain.base import YggdrasilEntity
from yggdrasil.domain.entities.artist import Artist
from yggdrasil.domain.entities.character import Character
from yggdrasil.domain.entities.file import File
from yggdrasil.domain.entities.group import Group
from yggdrasil.domain.entities.language import Language
from yggdrasil.domain.entities.language_info import LanguageInfo
from yggdrasil.domain.entities.language_localname import LanguageLocalname
from yggdrasil.domain.entities.parody import Parody
from yggdrasil.domain.entities.tag import Tag
from yggdrasil.domain.entities.type import Type


@dataclass
class Galleryinfo(YggdrasilEntity):
    date: datetime
    galleryurl: str
    id: int
    japanese_title: Optional[str]
    language_info: LanguageInfo
    language_localname: LanguageLocalname
    title: str
    type: Type
    video: Optional[str]
    videofilename: Optional[str]
    blocked: bool = field(default=False)
    datepublished: Optional[date] = field(default=None)
    artists: list[Artist] = field(default_factory=list[Artist])
    characters: list[Character] = field(default_factory=list[Character])
    files: list[File] = field(default_factory=list[File])
    groups: list[Group] = field(default_factory=list[Group])
    languages: list[Language] = field(default_factory=list[Language])
    parodys: list[Parody] = field(default_factory=list[Parody])
    related: list[int] = field(default_factory=list[int])
    scene_indexes: list[int] = field(default_factory=list[int])
    tags: list[Tag] = field(default_factory=list[Tag])
