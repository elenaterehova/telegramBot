from abc import ABC, abstractmethod, ABCMeta
import requests
import functools
from functools import lru_cache

from aiogram.types import URLInputFile

from DBConnector import DBConnector
from urllib.request import urlretrieve
import cachetools
from PIL import Image


class CacheInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def getInfoFromDB(self):
        """Get bot from DBConnector"""

    @abstractmethod
    def getNames(self):
        """Get all names from bot"""

    @abstractmethod
    def getCategories(self):
        """Get all categories from bot"""

    @abstractmethod
    def getProductByName(self, name):
        """Get """


class Cache(CacheInterface):

    def __init__(self):
        super().__init__()
        self.categories_names = None
        self.product_names = None

    # Получение всех товаров (возвращается словарь)
    @lru_cache(maxsize=256)
    def getInfoFromDB(self):
        data = DBConnector.getData(self)
        data1 = data.json()
        return data1

    # Получение всех названий (возвращается список)
    @lru_cache(maxsize=256)
    def getNames(self, name):
        data = Cache.getInfoFromDB(self)
        results = data['results']
        names = []
        for item in results:
            if name == item['properties']['Category']['select']['name']:
                products_name = item['properties']['Name']['title'][0]['text']['content']
                names.append(products_name)
        return names

    # Получение всех категорий (возвращается список)
    @lru_cache(maxsize=256)
    def getCategories(self):
        data = Cache.getInfoFromDB(self)
        results = data['results']
        categories_names = []
        for item in results:
            category = item['properties']['Category']['select']['name']
            categories_names.append(category)
        categories_names_list = []
        for x in categories_names:
            if x not in categories_names_list:
                categories_names_list.append(x)
        return categories_names_list

    # Получение товара по названию(возвращает словарь)
    @lru_cache(maxsize=256)
    def getProductByName(self, name):
        data = Cache.getInfoFromDB(self)
        results = data['results']
        for item in results:
            if name == item['properties']['Name']['title'][0]['text']['content']:
                url = item['properties']['Instructions']['files'][0]['file']['url']
                #photo = URLInputFile(url)
                return url


    @property
    def product_names_list(self):
        if self.product_names is None:
            self.product_names = Cache.getNames(set)
            return self.product_names

    @property
    def categories_names_list(self):
        if self.categories_names is None:
            self.categories_names = Cache.getCategories(set)
            return self.categories_names


cached_class = Cache()



