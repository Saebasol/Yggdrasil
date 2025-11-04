from dataclasses import dataclass

from yggdrasil.domain.entities.info import Info
from yggdrasil.domain.serializer import Serializer


@dataclass
class PostSearchQueryDTO:
    offset: int


@dataclass
class PostSearchBodyDTO:
    query: list[str]


@dataclass
class SearchResultDTO(Serializer):
    results: list[Info]
    count: int
