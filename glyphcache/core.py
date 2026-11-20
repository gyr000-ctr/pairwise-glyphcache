"""glyphcache 核心 API（初始未实现）。"""


class GlyphCache:
    def __init__(self, budget):
        """按字节预算构造"""
        raise NotImplementedError

    def get(self, glyph):
        """取字形位图"""
        raise NotImplementedError

    def bytes_used(self):
        """已用字节"""
        raise NotImplementedError

    def evictions(self):
        """淘汰次数"""
        raise NotImplementedError
