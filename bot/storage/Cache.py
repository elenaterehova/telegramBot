from abc import ABCMeta, abstractmethod, ABC
from io import BytesIO
import requests
from aiogram.types import BufferedInputFile


class CacheInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getNames(self, name):
        """Get all names from bot"""

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
    def get_product_by_name(self, product_name):
        pass


class Cache(CacheInterface, ABC):
    def __init__(self):
        super().__init__()

        # Фотки товаров
        self.__products = {}

        # Категории
        self.__categories = []

        # ключ – название категории
        # значение – список названий товаров
        self.__products_names = {}

    def get_names(self, category_name) -> [str]:
        return self.__products_names[category_name]

    def get_categories(self) -> [str]:
        return self.__categories

    def get_product_by_name(self, product_name) -> BytesIO:
        return self.__products[product_name]

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
            photo1 = requests.get(url).content
            photo = BufferedInputFile(photo1, filename='test')
            name = item['properties']['Name']['title'][0]['text']['content']
            self.__products[name] = photo
