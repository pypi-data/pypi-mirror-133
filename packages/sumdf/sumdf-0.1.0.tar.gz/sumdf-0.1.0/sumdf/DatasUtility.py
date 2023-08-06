import collections
import importlib
import itertools
import multiprocessing
import os

from sumdf import custom


class ParamSet(set):
    """Param container"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def unique(self, attr):
        """return unique value of attr"""
        return sorted(list(set(getattr(param, attr) for param in self)))


def tie(params, n=5):
    """tie parmas to regular expressions form

    Parameters
    ----------
    params : set of tuple
    n : int
        number of shuffle

    Note
    ----
    this is developing function
    """
    import copy
    import random

    bestD = None

    f = lambda D: sum(sum(map(len, _d)) for _d in D)

    for i in range(n):
        D = {tuple((elm,) for elm in param) for param in params}
        n = len(list(D)[0])
        indexes = list(range(n))
        if i > 0:
            random.shuffle(indexes)
        for j in range(n):
            res = tie_last_column(D, indexes)
            D = {tuple(keys[j] for j in range(n)) for keys in res}
            indexes = indexes[1:] + indexes[:1]
        if bestD is None or (len(D) < len(bestD) or (len(D) == len(bestD) and f(D) < f(bestD))):
            bestD = D

    # display
    string = f'#[{"][".join(custom.param_names)}]'
    for param in sorted(list(D)):
        s = ""
        for elm in param:
            if all(isinstance(key, int) for key in elm):
                elm = list(sorted(elm))
                new_elm = []
                while len(elm) > 1:
                    if elm[-1] == elm[0] + len(elm) - 1:
                        new_elm.append(f"{elm[0]}-{elm[-1]}")
                        elm = []
                    elif elm[1] > elm[0] + 1:
                        new_elm.append(elm[0])
                        elm = elm[1:]
                    else:
                        for i in range(len(elm) - 1):
                            if elm[i + 1] > elm[i] + 1:
                                new_elm.append(f"{elm[0]}-{elm[-1]}")
                                elm = elm[i + 1 :]
                                break
                if len(elm) == 1:
                    new_elm.append(elm[0])
                elm = new_elm
            s += f'[{",".join(map(str, elm))}]'
        string += '\n' + s
    return string


def tie_last_column(D, indexes):
    """tie parmas to regular expressions form

    Parameters
    ----------
    params : set of tuple
    indexes : list of int

    Returns
    -------
    list of dict
        res[i] = dict(key=index, value=tuple-values)
    """
    res = []
    while D:
        _D = D
        keys = dict()
        for i in indexes[:-1]:
            for d in _D:
                key = d[i]
                break
            _D = {d for d in _D if d[i] == key}
            keys[i] = key
        index = indexes[-1]
        keys[index] = tuple(sorted(list({d[index][0] for d in _D})))
        res.append(keys)
        D -= _D
    return res
