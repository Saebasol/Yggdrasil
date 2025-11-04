from dataclasses import dataclass
from typing import Optional

from yggdrasil.domain.base import YggdrasilEntity
from yggdrasil.domain.entities.language_info import LanguageInfo
from yggdrasil.domain.entities.language_localname import LanguageLocalname


@dataclass
class Language(YggdrasilEntity):
    galleryid: Optional[int]
    url: str
    language_localname: LanguageLocalname
    language_info: LanguageInfo
