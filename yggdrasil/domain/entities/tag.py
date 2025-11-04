from dataclasses import dataclass, field

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class Tag(YggdrasilEntity):
    tag: str
    url: str
    female: bool = field(default=False)
    male: bool = field(default=False)
