from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class Parody(YggdrasilEntity):
    parody: str
    url: str
