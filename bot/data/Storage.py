import PIL
from urllib.request import urlretrieve
from PIL import Image
import Cache
from abc import ABC, ABCMeta, abstractmethod
from Cache import Cache, cached_class


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
    def getNames(self, name):
        names = cached_class.getNames(name)
        return names

    def getCategories(self):
        categories = cached_class.categories_names_list
        return categories

    def getProductByName(self, name):
        product = cached_class.getProductByName(name)
        return product


storage_class = Storage()
