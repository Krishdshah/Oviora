from functools import lru_cache
@lru_cache(maxsize=256)
def memo(key:str): return key
