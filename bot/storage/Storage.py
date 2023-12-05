from abc import ABC, ABCMeta, abstractmethod
from bot.storage.Cache import Cache
from bot.storage.Cache import CacheInterface
from bot.storage.DBConnector import DBConnectorInterface, DBConnector


class StorageInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.id = None

    @abstractmethod
    def getNames(self, name):
        """Get cached names list from Cache Class"""

    @abstractmethod
    def getCategories(self):
        """Get cached categories list from Cache Class"""

    @abstractmethod
    def getProductByName(self, name):
        """Get cached product info by name"""


class Storage(StorageInterface, ABC):
    def __init__(self, cache: CacheInterface, db: DBConnectorInterface):
        super().__init__()
        self.cache = cache
        self.db = db
        self.request_count = 0

    def getInfoFromDB(self):
        data = self.db.getData()
        data1 = data.json()
        return data1

    def getNames(self, name):
        names = self.cache.get_names(category_name=name)

        if self.__update(data=names):
            names = self.cache.get_names(category_name=name)

        return names

    def getCategories(self):
        categories = self.cache.get_categories()
        if self.__update(data=categories):
            categories = self.cache.get_categories()
        return categories

    def getProductByName(self, name):
        product = self.cache.get_product_by_name(name)
        if self.__update(data=product):
            product = self.cache.get_product_by_name(name)
        return product

    def __update(self, data):
        self.request_count += 1
        if self.request_count > 5000 or data is None or (type(data) is list and len(data) == 0):
            data = self.db.getData().json()
            self.cache.update_data(json=data)
            self.request_count = 0
            return True
        return False


storage_class = Storage(cache=Cache(), db=DBConnector())
