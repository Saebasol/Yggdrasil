from copy import deepcopy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.domain.entities.conftest import sample_artist as sample_artist
from yggdrasil.domain.entities.artist import Artist
from yggdrasil.infrastructure.sqlalchemy.entities.artist import ArtistSchema
from yggdrasil.infrastructure.sqlalchemy.repositories.artist import SAArtistRepository


@pytest.mark.asyncio
async def test_get_or_add_artist_new_artist(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    artist = await artist_repository.get_or_add_artist(session, sample_artist)

    assert artist is not None
    assert isinstance(artist, ArtistSchema)


@pytest.mark.asyncio
async def test_get_or_add_artist_existing_artist(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    first = await artist_repository.get_or_add_artist(session, sample_artist)
    second = await artist_repository.get_or_add_artist(session, sample_artist)

    await session.commit()

    assert first == second


@pytest.mark.asyncio
async def test_get_or_add_artists_batch_with_existing_artist(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    existing_artist = deepcopy(sample_artist)
    existing_artist.artist = "artist_existing"
    existing_artist.url = "/artist/existing.html"

    new_artist = deepcopy(sample_artist)
    new_artist.artist = "artist_new"
    new_artist.url = "/artist/new.html"

    await artist_repository.get_or_add_artist(session, existing_artist)
    artists = await artist_repository.get_or_add_artists(
        session, [existing_artist, new_artist]
    )

    await session.commit()

    assert len(artists) == 2
    artist_pairs = {(artist.artist, artist.url) for artist in artists}
    assert ("artist_existing", "/artist/existing.html") in artist_pairs
    assert ("artist_new", "/artist/new.html") in artist_pairs


@pytest.mark.asyncio
async def test_get_all_artists_with_data(
    sample_artist: Artist, artist_repository: SAArtistRepository, session: AsyncSession
):
    artist1 = sample_artist
    artist1.artist = "artist_one"
    artist1.url = "/artist/one.html"
    artist2 = deepcopy(sample_artist)
    artist2.artist = "artist_two"
    artist2.url = "/artist/two.html"
    artist3 = deepcopy(sample_artist)
    artist3.artist = "artist_three"
    artist3.url = "/artist/three.html"

    await artist_repository.get_or_add_artist(session, artist1)
    await artist_repository.get_or_add_artist(session, artist2)
    await artist_repository.get_or_add_artist(session, artist3)

    await session.commit()

    artists = await artist_repository.get_all_artists()

    assert len(artists) == 3
    assert "artist_one" in artists
    assert "artist_two" in artists
    assert "artist_three" in artists
