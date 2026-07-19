from unittest.mock import AsyncMock

import pytest

from yggdrasil.application.usecases.create.deletion import (
    CreateGalleryinfoDeletionUseCase,
)
from yggdrasil.domain.exceptions import GalleryinfoNotFound


@pytest.fixture()
def deletion_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture()
def galleryinfo_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture()
def usecase(
    deletion_repository: AsyncMock,
    galleryinfo_repository: AsyncMock,
) -> CreateGalleryinfoDeletionUseCase:
    return CreateGalleryinfoDeletionUseCase(
        deletion_repository=deletion_repository,
        galleryinfo_repository=galleryinfo_repository,
    )


@pytest.mark.asyncio
async def test_create_galleryinfo_deletion(
    usecase: CreateGalleryinfoDeletionUseCase,
    deletion_repository: AsyncMock,
    galleryinfo_repository: AsyncMock,
):
    galleryinfo_id = 1
    galleryinfo_repository.is_galleryinfo_exists.return_value = True

    await usecase.execute(galleryinfo_id)

    galleryinfo_repository.is_galleryinfo_exists.assert_awaited_once_with(
        galleryinfo_id
    )
    deletion_repository.add_galleryinfo_deletion.assert_awaited_once_with(
        galleryinfo_id
    )


@pytest.mark.asyncio
async def test_create_galleryinfo_deletion_for_nonexistent_galleryinfo(
    usecase: CreateGalleryinfoDeletionUseCase,
    deletion_repository: AsyncMock,
    galleryinfo_repository: AsyncMock,
):
    galleryinfo_id = 1
    galleryinfo_repository.is_galleryinfo_exists.return_value = False

    with pytest.raises(GalleryinfoNotFound):
        await usecase.execute(galleryinfo_id)

    galleryinfo_repository.is_galleryinfo_exists.assert_awaited_once_with(
        galleryinfo_id
    )
    deletion_repository.add_galleryinfo_deletion.assert_not_awaited()
