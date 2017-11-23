import collections
import itertools
from . import stats

__all__ = [
    'Party',
    'HoR',
    'Coalition'
]

Party = collections.namedtuple('Party', 'name,votes,seats')


class HoR(object):
    """House of Representatives"""

    def __init__(self, parties):
        self._parties = list(sorted(parties, key=lambda p: (p.seats, p.votes), reverse=True))

    @property
    def parties(self):
        return self._parties

    def seats_list(self):
        return [p.seats for p in self._parties]

    def votes_list(self):
        return [p.votes for p in self._parties]

    def names_list(self):
        return [p.name for p in self._parties]

    def vote_shares_list(self):
        v = self.votes
        return [vi / v for vi in self.votes_list()]

    def seat_shares_list(self):
        s = self.seats
        return [si / s for si in self.seats_list()]

    @property
    def seats(self):
        return sum(self.seats_list())

    @property
    def votes(self):
        return sum(self.votes_list())

    def top(self, n=1):
        return Coalition(self, self._parties[:n])

    def as_coalition(self):
        return Coalition(self, self._parties)

    def __contains__(self, item):
        return item in self._parties

    def __iter__(self):
        return iter(self._parties)

    def iter_coalitions(self):
        for n in range(1, len(self)):
            for coalition in itertools.combinations(self._parties, n):
                yield Coalition(self, coalition)

    def __len__(self):
        return len(self._parties)

    def same_as(self, hor):
        return self.parties == hor.parties

    def __eq__(self, other):
        return self.seats == other.seats

    def __gt__(self, other):
        return self.seats > other.seats

    def __ge__(self, other):
        return self.seats >= other.seats

    def __le__(self, other):
        return self.seats <= other.seats

    def __lt__(self, other):
        return self.seats < other.seats

    haar = stats.haar
    dev = stats.dev
    ens = stats.ens
    env = stats.env
    rrp = stats.rrp
    bantsaf_influence = stats.bantsaf_influence
    shepli_shubic = stats.shepli_shubic
    jonson_general = stats.jonson_general
    jonson_influence = stats.jonson_influence
    digen_pakel_general = stats.digen_pakel_general
    digen_pakel_influence = stats.digen_pakel_influence
    holer_pakel = stats.holer_pakel


class Coalition(HoR):
    def __init__(self, hor, parties, *, _opposition=None):
        super().__init__(parties)
        self._hor = hor
        self._opposition = _opposition

    @property
    def opposition(self):
        if self._opposition is None:
            others = [p for p in self._hor if p not in self]
            self._opposition = Coalition(self._hor, others, _opposition=self)
        return self._opposition

    @property
    def hor(self):
        return self._hor

    def __add__(self, other):
        if isinstance(other, Party):
            if other in self:
                raise ValueError('{} is already present in HoR'.format(other))
            new = self._parties + [other]
        elif isinstance(other, Coalition) and other.hor.same_as(self.hor):
            intercept = set(other) & set(self._parties)
            if intercept:
                raise ValueError('{} are already present in HoR'.format(intercept))
            new = self._parties + list(other)
        else:
            raise TypeError('Wrong type for {}'.format(other))
        return self.__class__(self.hor, new)

    def __sub__(self, other):
        if isinstance(other, Party):
            if other not in self:
                raise ValueError('{} is not present in HoR'.format(other))
            new = set(self._parties) - {other}
        elif isinstance(other, Coalition) and other.hor.same_as(self.hor):
            intercept = set(other) & set(self._parties)
            if not intercept:
                raise ValueError('{} are not present in HoR'.format(intercept))
            new = set(self._parties) - set(other.parties)
        else:
            raise TypeError('Wrong type for {}'.format(other))
        return self.__class__(self.hor, new)

    def has_key_party(self, party):
        if party not in self:
            return False
        else:
            opposition = self.opposition
            return (
                (self > opposition)
                and
                ((self - party) <= (opposition + party))
            )

    def key_parties(self):
        return list(filter(self.has_key_party, self.parties))

    def is_minimum_winning(self):
        return all(map(self.has_key_party, self.parties))

