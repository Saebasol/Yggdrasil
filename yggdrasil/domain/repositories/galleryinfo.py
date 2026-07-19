from abc import ABC, abstractmethod
from typing import Optional

from yggdrasil.domain.entities.galleryinfo import Galleryinfo


class GalleryinfoRepository(ABC):
    @abstractmethod
    async def get_galleryinfo(self, id: int) -> Optional[Galleryinfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_galleryinfo_without_deleted(self, id: int) -> Optional[Galleryinfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_galleryinfo_ids(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_galleryinfo_ids_without_deleted(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def add_galleryinfo(self, galleryinfo: Galleryinfo) -> int:
        raise NotImplementedError

    @abstractmethod
    async def is_galleryinfo_exists(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_galleryinfo(self, id: int) -> None:
        """Soft-delete a galleryinfo while preserving its source record."""
        raise NotImplementedError
