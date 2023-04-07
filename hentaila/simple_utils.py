from . import _base


def _base_func(x):
    return x.get("href")


def iter_base_func(x):
    return _base + x.get("href")
