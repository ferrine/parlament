import pytest

from parlament.core import Coalition


def test_add(parties, hor):
    coal = Coalition(hor, parties[:2])
    with pytest.raises(ValueError) as e:
        coal + parties[1]
        assert e.match_expr('is already present')
    coalp1 = coal + parties[2]
    coal_true = Coalition(hor, parties[:3])
    assert coalp1.same_as(coal_true)
    assert not coal.same_as(coal_true)

    coal2 = Coalition(hor, parties[2:])
    assert coal2.same_as(coal.opposition)
    coal_big = coal+coal2
    assert coal_big.same_as(hor)


def test_sub(parties, hor):
    coal = Coalition(hor, parties[:2])
    with pytest.raises(ValueError) as e:
        coal - parties[2]
        assert e.match_expr('is not present')
    coalm1 = coal - parties[1]
    coal_true = Coalition(hor, parties[:1])
    assert coalm1.same_as(coal_true)
    assert not coal.same_as(coal_true)


def test_key_parties(parties, hor):
    assert [] == hor.as_coalition().key_parties()
    coalition = Coalition(hor, parties[1:])
    assert parties[-1:] == coalition.key_parties()
    coalition = Coalition(hor, parties[2:])
    assert coalition.is_minimum_winning()
    coalition = Coalition(hor, parties[:2])
    assert not coalition.is_minimum_winning()

