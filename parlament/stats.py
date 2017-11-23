
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

