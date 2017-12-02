import pytest

from parliament.core import Party, HoR


@pytest.fixture('session')
def parties(): return [
    Party('first', 1100, 10),
    Party('second', 2000, 20),
    Party('third', 3300, 30),
    Party('fourth', 4500, 41)
]


@pytest.fixture('session')
def hor(parties):
    return HoR(parties)
