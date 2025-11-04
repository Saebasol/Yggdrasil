from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class Character(YggdrasilEntity):
    character: str
    url: str
