from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity
from yggdrasil.domain.entities.file import File


@dataclass
class ResolvedImage(YggdrasilEntity):
    url: str
    file: File
