from parlament import stats


import numpy as np


def test_haar(hor):
    true = (1100 + 2000 + 3300 + 4500) / (10 + 20 + 30 + 41)
    assert stats.haar(hor) == true


def test_env(hor):
    v = (1100 + 2000 + 3300 + 4500)
    vi = (1100/v,  2000/v, 3300/v,  4500/v)
    true = 1/sum(_vi**2 for _vi in vi)
    assert np.allclose(stats.env(hor),  true)


def test_ens(hor):
    s = (10 + 20 + 30 + 41)
    si = (10 / s, 20 / s, 30 / s, 41 / s)
    true = 1 / sum(_si ** 2 for _si in si)
    assert np.allclose(stats.ens(hor), true)


def test_dev(hor):
    v = (1100 + 2000 + 3300 + 4500)
    vi = (1100 / v, 2000 / v, 3300 / v, 4500 / v)

    s = (10 + 20 + 30 + 41)
    si = (10 / s, 20 / s, 30 / s, 41 / s)

    asvi = tuple(map(abs, ((_si - _vi) for (_si, _vi) in zip(si, vi))))
    true = sum(asvi) / 2
    assert np.allclose(stats.dev(hor), true)


def test_rrp(hor):
    _env = stats.env(hor)
    _ens = stats.ens(hor)
    true = (_env - _ens) / _ens * 100
    assert stats.rrp(hor) == true

