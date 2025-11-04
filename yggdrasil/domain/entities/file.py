from dataclasses import dataclass, field

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class File(YggdrasilEntity):
    hasavif: bool
    hash: str
    height: int
    name: str
    width: int
    hasjxl: bool = field(default=False)
    haswebp: bool = field(default=False)
    single: bool = field(default=False)
