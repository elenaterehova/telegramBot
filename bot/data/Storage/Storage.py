from abc import ABC, ABCMeta, abstractmethod
from bot.data.Storage.Cache import Cache
from bot.data.Storage.Cache import CacheInterface


class StorageInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.id = None

    @abstractmethod
    def getNames(self):
        """Get cached names list from Cache Class"""

    @abstractmethod
    def getCategories(self):
        """Get cached categories list from Cache Class"""

    @abstractmethod
    def getProductByName(self, name):
        """Get cached product info by name"""


class Storage(StorageInterface, ABC):
    def __init__(self, cache: CacheInterface):
        self.cache = cache

    def getNames(self, name):
        names = self.cache.getNames(name)
        return names

    def getCategories(self):
        categories = self.cache.categories_names_list
        return categories

    def getProductByName(self, name):
        product = self.cache.getProductByName(name)
        return product


storage_class = Storage(cache=Cache())
