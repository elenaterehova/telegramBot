import os
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('token')
database_id = os.getenv('database_id')
url = os.getenv('url')
headers = {
    'Authorization': f'Bearer {token}',
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}


class DBConnectorInterface(ABC):

    @abstractmethod
    def getData(self):
        """Get bot from DB"""


class DBConnector(DBConnectorInterface):
    def getData(self):
        response = requests.post(url, headers=headers)
        return response
