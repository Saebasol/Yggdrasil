from abc import ABC, abstractmethod


class DeletionRepository(ABC):
    @abstractmethod
    async def get_deleted_galleryinfo_ids(self) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def is_galleryinfo_deleted(self, galleryinfo_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add_galleryinfo_deletion(self, galleryinfo_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_galleryinfo_deletion(self, galleryinfo_id: int) -> None:
        raise NotImplementedError
