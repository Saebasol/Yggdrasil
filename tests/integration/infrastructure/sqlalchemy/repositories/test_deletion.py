import pytest

from tests.unit.domain.entities.conftest import sample_galleryinfo as sample_galleryinfo
from yggdrasil.domain.entities.galleryinfo import Galleryinfo
from yggdrasil.infrastructure.sqlalchemy.repositories.deletion import (
    SADeletionRepository,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.galleryinfo import (
    SAGalleryinfoRepository,
)


@pytest.mark.asyncio
async def test_add_and_remove_galleryinfo_deletion(
    sample_galleryinfo: Galleryinfo,
    galleryinfo_repository: SAGalleryinfoRepository,
    deletion_repository: SADeletionRepository,
):
    await galleryinfo_repository.add_galleryinfo(sample_galleryinfo)

    await deletion_repository.add_galleryinfo_deletion(sample_galleryinfo.id)
    await deletion_repository.add_galleryinfo_deletion(sample_galleryinfo.id)

    assert await deletion_repository.is_galleryinfo_deleted(sample_galleryinfo.id)
    assert await deletion_repository.get_deleted_galleryinfo_ids() == [
        sample_galleryinfo.id
    ]

    await deletion_repository.delete_galleryinfo_deletion(sample_galleryinfo.id)

    assert not await deletion_repository.is_galleryinfo_deleted(sample_galleryinfo.id)
