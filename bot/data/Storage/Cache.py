from abc import ABC, abstractmethod, ABCMeta
import requests
import functools
from functools import lru_cache

from aiogram.types import URLInputFile
from bot.data.Storage.DBConnector import *
from urllib.request import urlretrieve
import cachetools
from PIL import Image


class CacheInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getInfoFromDB(self):
        """Get bot from DBConnector"""

    @abstractmethod
    def getNames(self, name):
        """Get all names from bot"""

    @abstractmethod
    def getCategories(self):
        """Get all categories from bot"""

    @abstractmethod
    def getProductByName(self, name):
        """Get """

    @abstractmethod
    def get_categories(self):
        """Get categories list"""

    @abstractmethod
    def update_data(self, json):
        """Update data"""

    @abstractmethod
    def get_names(self, category_name):
        pass

    @abstractmethod
    def get_product_by_name(self, product_name) -> URLInputFile:
        pass


class Cache(CacheInterface):
    def __init__(self):
        super().__init__()
        self.categories_names = None
        self.product_names = None
        # Фотки товаров
        self.__products = {}

        # Категории
        self.__categories = []

        # ключ – название категории
        # значение – список названий товаров
        self.__products_names = {}

    # # Получение всех названий (возвращается список)
    # @lru_cache(maxsize=256)
    # def getNames(self, category_name):
    #     data = Cache.getInfoFromDB(self)
    #     results = data['results']
    #     names = []
    #     for item in results:
    #         if category_name == item['properties']['Category']['select']['name']:
    #             products_name = item['properties']['Name']['title'][0]['text']['content']
    #             names.append(products_name)
    #     return names

    def get_names(self, category_name) -> [str]:
        return self.__products_names[category_name]

    def get_categories(self) -> [str]:
        return self.__categories

    def get_product_by_name(self, product_name) -> URLInputFile:
        return self.__products[product_name]

    # Получение товара по названию(возвращает словарь)
    # @lru_cache(maxsize=256)
    def getProductByName(self, name):
        if name in self.__products.keys() and type(self.__products[name]) is URLInputFile:
            return self.__products[name]

        data = Cache.getInfoFromDB(self)
        results = data['results']
        for item in results:
            if name == item['properties']['Name']['title'][0]['text']['content']:
                url = item['properties']['Instructions']['files'][0]['file']['url']
                photo = URLInputFile(url)
                self.__products[name] = photo
                return photo

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

    def update_data(self, json):
        self.__update_categories(data=json)
        self.__update_names(data=json)
        self.__update_products(data=json)

    def __update_categories(self, data):
        results = data['results']
        categories_names = []
        for item in results:
            category = item['properties']['Category']['select']['name']
            categories_names.append(category)
        categories_names_list = []
        for x in categories_names:
            if x not in categories_names_list:
                categories_names_list.append(x)

        self.__categories = categories_names_list

    def __update_names(self, data):
        results = data['results']
        self.__products_names = {}
        
        for item in results:
            category_name = item['properties']['Category']['select']['name']
            product_name = item['properties']['Name']['title'][0]['text']['content']
            
            if category_name in self.__products_names.keys():
                # Если название категории уже добавлено в словарь
                self.__products_names[category_name].append(product_name)
            else:
                # Если название категории не добавлено
                self.__products_names[category_name] = [product_name]

        print(self.__products_names)

    def __update_products(self, data):
        results = data['results']
        for item in results:
            url = item['properties']['Instructions']['files'][0]['file']['url']
            photo = URLInputFile(url)
            name = item['properties']['Name']['title'][0]['text']['content']
            self.__products[name] = photo



cached_class = Cache()
