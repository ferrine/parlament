import functools
import collections
import tabulate
import math

__all__ = [
    'haar',
    'dev',
    'ens',
    'env',
    'rrp',
    'bantsaf_influence',
    'shepli_shubic',
    'jonson_general',
    'jonson_influence',
    'digen_pakel_general',
    'digen_pakel_influence',
    'holer_pakel'
]


def haar(hor):
    return hor.votes / hor.seats


def env(hor):
    return 1/sum(svi ** 2 for svi in hor.vote_shares_list())


def ens(hor):
    return 1/sum(ssi ** 2 for ssi in hor.seat_shares_list())


def dev(hor):
    return .5 * sum(
        abs(ssi - svi)
        for ssi, svi in
        zip(hor.seat_shares_list(), hor.vote_shares_list())
    )


def rrp(hor):
    _env = env(hor)
    _ens = ens(hor)
    return (_env - _ens) / _ens * 100


@functools.lru_cache(maxsize=None)
def bantsaf_influence(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    bi = collections.Counter()
    for coalition in hor.iter_coalitions():
        for p in coalition.key_parties():
            bi[p] += 1
    return bi[party] / sum(bi.values())


@functools.lru_cache(maxsize=None)
def shepli_shubic(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    n = len(hor)
    res = 0
    for coalition in hor.iter_coalitions():
        if coalition.has_key_party(party):
            res += math.factorial(len(coalition) - 1)*math.factorial(n - len(coalition))
    return res/math.factorial(n)


@functools.lru_cache(maxsize=None)
def jonson_general(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    res = 0
    for coalition in hor.iter_coalitions():
        if coalition.has_key_party(party):
            res += 1 / len(coalition.key_parties())
    return res


def jonson_influence(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    jg = {p: jonson_general(hor, p) for p in hor.parties}
    return jg[party] / sum(jg.values())


@functools.lru_cache(maxsize=None)
def digen_pakel_general(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    res = 0
    for coalition in hor.iter_coalitions():
        if party in coalition and coalition.is_minimum_winning():
            res += 1 / len(coalition)
    return res


def digen_pakel_influence(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    dpg = {p: digen_pakel_general(hor, p) for p in hor.parties}
    return dpg[party] / sum(dpg.values())


@functools.lru_cache(maxsize=None)
def holer_pakel(hor, party):
    if party not in hor:
        raise ValueError('{} not in HoR'.format(party))
    hpi = collections.Counter()
    for coalition in hor.iter_coalitions():
        if coalition.is_minimum_winning():
            for p in coalition.parties:
                hpi[p] += 1
    return hpi[party] / sum(hpi.values())


def describe(hor, **tab_kw):
    res = ""
    rows = list()
    head = ['', 'seats', 'parties', 'haar', 'dev', 'ens', 'env', 'rrp']
    rows.append(['HoR', int(hor.seats), len(hor), hor.haar(), hor.dev(), hor.ens(), hor.env(), hor.rrp()])
    res += tabulate.tabulate(rows, headers=head, **tab_kw)
    res += '\n\n'
    head = [
        'name',
        'votes',
        'seats',
        'bantsaf_influence',
        'shepli_shubic',
        'jonson_general',
        'jonson_influence',
        'digen_pakel_general',
        'digen_pakel_influence',
        'holer_pakel'
    ]
    rows = list()
    for party in hor.parties:
        rows.append([
            party.name,
            int(party.votes),
            int(party.seats),
            hor.bantsaf_influence(party),
            hor.shepli_shubic(party),
            hor.jonson_general(party),
            hor.jonson_influence(party),
            hor.digen_pakel_general(party),
            hor.digen_pakel_influence(party),
            hor.holer_pakel(party)
        ])
    res += tabulate.tabulate(rows, headers=head, **tab_kw)
    return res

