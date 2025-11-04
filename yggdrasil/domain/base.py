from __future__ import annotations

from yggdrasil.domain.deserializer import Deserializer
from yggdrasil.domain.serializer import Serializer


class BaseYggdrasil: ...


class YggdrasilEntity(BaseYggdrasil, Serializer, Deserializer): ...
