from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.domain.entities.conftest import (
    sample_language_localname as sample_language_localname,
)
from yggdrasil.domain.entities.language_localname import LanguageLocalname
from yggdrasil.infrastructure.sqlalchemy.entities.language_localname import (
    LanguageLocalnameSchema,
)
from yggdrasil.infrastructure.sqlalchemy.repositories.language_localname import (
    SALanguageLocalnameRepository,
)


@pytest.mark.asyncio
async def test_get_or_add_language_localname_new_language_localname(
    sample_language_localname: LanguageLocalname,
    language_localname_repository: SALanguageLocalnameRepository,
    session: AsyncSession,
):
    language_localname = (
        await language_localname_repository.get_or_add_language_localname(
            session, sample_language_localname
        )
    )

    assert language_localname is not None
    assert isinstance(language_localname, LanguageLocalnameSchema)


@pytest.mark.asyncio
async def test_get_or_add_language_localname_existing_language_localname(
    sample_language_localname: LanguageLocalname,
    language_localname_repository: SALanguageLocalnameRepository,
    session: AsyncSession,
):
    first_id = await language_localname_repository.get_or_add_language_localname(
        session, sample_language_localname
    )
    second_id = await language_localname_repository.get_or_add_language_localname(
        session, sample_language_localname
    )

    assert first_id == second_id


@pytest.mark.asyncio
async def test_get_or_add_language_localnames_batch_with_existing_localname(
    sample_language_localname: LanguageLocalname,
    language_localname_repository: SALanguageLocalnameRepository,
    session: AsyncSession,
):
    existing_localname = deepcopy(sample_language_localname)
    existing_localname.name = "日本語"

    new_localname = deepcopy(sample_language_localname)
    new_localname.name = "English"

    await language_localname_repository.get_or_add_language_localname(
        session, existing_localname
    )
    localnames = await language_localname_repository.get_or_add_language_localnames(
        session, [existing_localname, new_localname]
    )

    await session.commit()

    assert len(localnames) == 2
    localname_names = {localname.name for localname in localnames}
    assert "日本語" in localname_names
    assert "English" in localname_names
