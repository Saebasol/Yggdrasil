from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.domain.entities.conftest import sample_artist as sample_artist
from yggdrasil.domain.entities.parody import Parody
from yggdrasil.infrastructure.sqlalchemy.entities.parody import ParodySchema
from yggdrasil.infrastructure.sqlalchemy.repositories.parody import SAParodyRepository


@pytest.mark.asyncio
async def test_get_or_add_parody_new_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    parody = await parody_repository.get_or_add_parody(session, sample_parody)

    assert parody is not None
    assert isinstance(parody, ParodySchema)


@pytest.mark.asyncio
async def test_get_or_add_parody_existing_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    first = await parody_repository.get_or_add_parody(session, sample_parody)
    second = await parody_repository.get_or_add_parody(session, sample_parody)

    await session.commit()

    assert first == second


@pytest.mark.asyncio
async def test_get_or_add_parodies_batch_with_existing_parody(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    existing_parody = deepcopy(sample_parody)
    existing_parody.parody = "parody_existing"
    existing_parody.url = "/parody/existing.html"

    new_parody = deepcopy(sample_parody)
    new_parody.parody = "parody_new"
    new_parody.url = "/parody/new.html"

    await parody_repository.get_or_add_parody(session, existing_parody)
    parodies = await parody_repository.get_or_add_parodies(
        session, [existing_parody, new_parody]
    )

    await session.commit()

    assert len(parodies) == 2
    parody_pairs = {(parody.parody, parody.url) for parody in parodies}
    assert ("parody_existing", "/parody/existing.html") in parody_pairs
    assert ("parody_new", "/parody/new.html") in parody_pairs


@pytest.mark.asyncio
async def test_get_all_parodies_with_data(
    sample_parody: Parody, parody_repository: SAParodyRepository, session: AsyncSession
):
    parody1 = sample_parody
    parody1.parody = "parody_one"
    parody1.url = "/parody/one.html"
    parody2 = deepcopy(sample_parody)
    parody2.parody = "parody_two"
    parody2.url = "/parody/two.html"
    parody3 = deepcopy(sample_parody)
    parody3.parody = "parody_three"
    parody3.url = "/parody/three.html"

    await parody_repository.get_or_add_parody(session, parody1)
    await parody_repository.get_or_add_parody(session, parody2)
    await parody_repository.get_or_add_parody(session, parody3)

    await session.commit()

    parodies = await parody_repository.get_all_parodies()

    assert len(parodies) == 3
    assert "parody_one" in parodies
    assert "parody_two" in parodies
    assert "parody_three" in parodies
