import pytest

from raga.models import Raga, Tala, load_ragas, load_talas


@pytest.fixture(scope="session")
def ragas() -> list[Raga]:
    return load_ragas()


@pytest.fixture(scope="session")
def talas() -> list[Tala]:
    return load_talas()
