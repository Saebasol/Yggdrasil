from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class AllTags(YggdrasilEntity):
    artists: list[str]
    characters: list[str]
    groups: list[str]
    language: list[str]
    series: list[str]
    tag: list[str]
    female: list[str]
    male: list[str]
    type: list[str]
