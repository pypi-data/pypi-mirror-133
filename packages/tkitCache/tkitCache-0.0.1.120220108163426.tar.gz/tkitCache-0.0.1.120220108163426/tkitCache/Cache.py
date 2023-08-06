# -*- coding: utf-8 -*-
"""
作者：　terrychan
Blog: https://terrychan.org
# 说明：

"""
import os
# from cacheout import Cache
# from cacheout import Cache# 如果选择LFUCache 就导入即可
from cacheout import LFUCache


class tkitCache():
    def __init__(self):
        self.cache = LFUCache()
        pass

    def set(self, key, value):
        self.cache.set(key, value)

    def set_many(self, data: dict):
        self.cache.set_many(data)

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        return self.cache.delete(key)

    def delete_many(self, keys: list):
        return self.cache.delete_many(keys)

    def clear(self):
        return self.cache.clear()
    def get_all(self):
        for key in self.cache.keys():
            # print(key)
            yield self.get(key)
            pass


if __name__ == '__main__':
    c = tkitCache()
    # c.cache.set(1,'www')
    # print(c.cache.get(1))
    c.set(1, {"ede": 22})
    print(c.get(1))
    # print(c.get_all())
    for it in c.get_all():
        print(it)
    pass
