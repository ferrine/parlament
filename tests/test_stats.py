from parliament import stats, HoR, Party


import numpy as np


def test_haar(hor):
    true = (1100 + 2000 + 3300 + 4500) / (10 + 20 + 30 + 41)
    assert stats.haar(hor) == true


def test_env(hor):
    v = (1100 + 2000 + 3300 + 4500)
    vi = (1100/v,  2000/v, 3300/v,  4500/v)
    true = 1/sum(_vi**2 for _vi in vi)
    assert np.allclose(stats.env(hor),  true)
    assert np.allclose(hor.env(), true)


def test_ens(hor):
    s = (10 + 20 + 30 + 41)
    si = (10 / s, 20 / s, 30 / s, 41 / s)
    true = 1 / sum(_si ** 2 for _si in si)
    assert np.allclose(stats.ens(hor), true)
    assert np.allclose(hor.ens(), true)


def test_dev(hor):
    v = (1100 + 2000 + 3300 + 4500)
    vi = (1100 / v, 2000 / v, 3300 / v, 4500 / v)

    s = (10 + 20 + 30 + 41)
    si = (10 / s, 20 / s, 30 / s, 41 / s)

    asvi = tuple(map(abs, ((_si - _vi) for (_si, _vi) in zip(si, vi))))
    true = sum(asvi) / 2
    assert np.allclose(stats.dev(hor), true)
    assert np.allclose(hor.dev(), true)


def test_rrp(hor):
    _env = stats.env(hor)
    _ens = stats.ens(hor)
    true = (_env - _ens) / _ens * 100
    assert stats.rrp(hor) == true
    assert hor.rrp() == true


def test_bantsaf():
    # 5, 10, 20, 30, 35
    parties = [
        Party(1, 1, 5),
        Party(2, 1, 10),
        Party(3, 1, 20),
        Party(4, 1, 30),
        Party(5, 1, 35)
    ]
    hor = HoR(parties)
    true = [1/25, 1/25, 7/25, 7/25, 9/25]
    test = [hor.bantsaf_influence(p) for p in parties]
    assert test == true


def test_shepli():
    # 5, 10, 20, 30, 35
    parties = [
        Party(1, 1, 5),
        Party(2, 1, 10),
        Party(3, 1, 20),
        Party(4, 1, 30),
        Party(5, 1, 35)
    ]
    hor = HoR(parties)
    true = [2/60, 2/60, 17/60, 17/60, 22/60]
    test = [hor.shepli_shubic(p) for p in parties]
    assert test == true
