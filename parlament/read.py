from .core import HoR, Party

__all__ = ['hor_from_df']


def hor_from_df(d, name='name', votes='votes', seats='seats', *, nonzero=True):
    names = d[name]
    votes = d[votes]
    seats = d[seats]
    if nonzero:
        return HoR(Party(n, v, s) for n, v, s in zip(names, votes, seats) if s > 0)
    else:
        return HoR(Party(n, v, s) for n, v, s in zip(names, votes, seats))
