from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class Type(YggdrasilEntity):
    type: str
