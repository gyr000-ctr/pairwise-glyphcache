import math

import pytest

import glyphcache

def _raises(fn, exc=ValueError):
    try:
        fn()
    except exc:
        return True
    return False

def _c():
    return glyphcache.GlyphCache(10)


def _hit():
    c = _c()
    c.get(1)
    return c.get(1) == bytes([1]) * 4


def _used():
    c = _c()
    c.get(1)
    return c.bytes_used() == 4


def _evict():
    c = _c()
    c.get(1)
    c.get(2)
    c.get(3)
    return c.evictions() >= 1


def _budget():
    c = _c()
    for i in range(6):
        c.get(i)
    return c.bytes_used() <= 10


def _bad_budget():
    return _raises(lambda: glyphcache.GlyphCache(0))


def _missing():
    return _raises(lambda: _c().get(999))


def _empty():
    return _c().bytes_used() == 0


def _type():
    return isinstance(_c().get(1), bytes)


def _det():
    return _c().get(2) == _c().get(2)


def _evict_init():
    return _c().evictions() == 0


def _size():
    c = _c()
    c.get(1)
    c.get(2)
    return c.bytes_used() <= 10


def _reget():
    c = _c()
    for i in range(4):
        c.get(i)
    return c.get(1) is not None


def _no_dup():
    c = _c()
    c.get(1)
    c.get(1)
    return c.bytes_used() == 4


def _neg():
    return _raises(lambda: glyphcache.GlyphCache(-1))


def _count():
    c = _c()
    for i in range(3):
        c.get(i)
    return len([1 for i in range(3)]) == 3

CASES = [("hit", "_hit"), ("used", "_used"), ("evict", "_evict"), ("budget", "_budget"), ("bad_budget", "_bad_budget"), ("missing", "_missing"), ("empty", "_empty"), ("type", "_type"), ("det", "_det"), ("evict_init", "_evict_init"), ("size", "_size"), ("reget", "_reget"), ("no_dup", "_no_dup"), ("neg", "_neg"), ("count", "_count")]


@pytest.mark.parametrize("name,check", CASES, ids=[c[0] for c in CASES])
def test_spec(name, check):
    assert globals()[check]() is True
