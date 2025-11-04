from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class Group(YggdrasilEntity):
    group: str
    url: str
