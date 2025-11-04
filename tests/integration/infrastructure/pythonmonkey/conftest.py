import pytest_asyncio

from tests.integration.infrastructure.hitomila.conftest import hitomi_la as hitomi_la
from yggdrasil.infrastructure.hitomila import HitomiLa
from yggdrasil.infrastructure.pythonmonkey import JavaScriptInterpreter


@pytest_asyncio.fixture()
async def javascript_interpreter(hitomi_la: HitomiLa):
    interpreter = await JavaScriptInterpreter.setup(hitomi_la)
    yield interpreter
