from dataclasses import dataclass

from yggdrasil.domain.base import YggdrasilEntity


@dataclass
class LanguageInfo(YggdrasilEntity):
    language: str
    language_url: str
