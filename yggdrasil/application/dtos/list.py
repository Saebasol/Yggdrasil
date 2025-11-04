from dataclasses import dataclass

from yggdrasil.domain.entities.info import Info
from yggdrasil.domain.serializer import Serializer


@dataclass
class ListResultDTO(Serializer):
    items: list[Info]
    count: int
