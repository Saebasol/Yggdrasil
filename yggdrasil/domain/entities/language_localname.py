from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class LanguageLocalname(YggdrasilEntity):
    name: str
