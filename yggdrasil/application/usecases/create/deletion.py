from yggdrasil.domain.exceptions import GalleryinfoNotFound
from yggdrasil.domain.repositories.deletion import DeletionRepository
from yggdrasil.domain.repositories.galleryinfo import GalleryinfoRepository


class CreateGalleryinfoDeletionUseCase:
    def __init__(
        self,
        deletion_repository: DeletionRepository,
        galleryinfo_repository: GalleryinfoRepository,
    ) -> None:
        self.deletion_repository = deletion_repository
        self.galleryinfo_repository = galleryinfo_repository

    async def execute(self, galleryinfo_id: int) -> None:
        if not await self.galleryinfo_repository.is_galleryinfo_exists(
            galleryinfo_id
        ):
            raise GalleryinfoNotFound.from_id(galleryinfo_id)

        await self.deletion_repository.add_galleryinfo_deletion(galleryinfo_id)
