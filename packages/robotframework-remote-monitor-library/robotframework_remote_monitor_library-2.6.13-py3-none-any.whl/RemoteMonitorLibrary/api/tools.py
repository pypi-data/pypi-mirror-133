from typing import List

from ..model.errors import RunnerError
from ..utils import Singleton
from ..utils.collections import CacheList


@Singleton
class GlobalErrors(list, List[RunnerError]):
    def __init__(self):
        list.__init__(self)


__all__ = [
    'CacheList',
    'GlobalErrors'
]
