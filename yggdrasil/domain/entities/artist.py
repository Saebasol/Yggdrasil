from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class Artist(YggdrasilEntity):
    artist: str
    url: str
