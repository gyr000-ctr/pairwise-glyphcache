"""glyphcache 核心 API：按字节预算的字形位图 LRU 缓存。"""

import threading
from collections import OrderedDict

__all__ = ["GlyphCache"]


def _decode(glyph):
    """解码字形位图（确定性）；非法字形由 bytes() 抛出 ValueError。"""
    return bytes([glyph]) * 4


class GlyphCache:
    def __init__(self, budget):
        """按字节预算构造"""
        if not isinstance(budget, int) or isinstance(budget, bool) or budget <= 0:
            raise ValueError("budget must be a positive integer")
        self._budget = budget
        self._cache = OrderedDict()  # glyph -> bitmap, 按最近使用排序
        self._used = 0
        self._evictions = 0
        self._lock = threading.Lock()

    def get(self, glyph):
        """取字形位图；命中不重复解码，未命中解码后按 LRU 缓存"""
        with self._lock:
            bitmap = self._cache.get(glyph)
            if bitmap is not None:
                self._cache.move_to_end(glyph)
                return bitmap
            bitmap = _decode(glyph)  # 非法字形在此抛 ValueError，不改变缓存状态
            size = len(bitmap)
            if size > self._budget:
                # 大字形超预算：不缓存，直接返回，结果与禁用缓存一致
                return bitmap
            while self._used + size > self._budget:
                _, old = self._cache.popitem(last=False)  # 淘汰最久未使用
                self._used -= len(old)
                self._evictions += 1
            self._cache[glyph] = bitmap
            self._used += size
            return bitmap

    def bytes_used(self):
        """已用字节"""
        with self._lock:
            return self._used

    def evictions(self):
        """淘汰次数"""
        with self._lock:
            return self._evictions
