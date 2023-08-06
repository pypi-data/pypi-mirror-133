import requests


class Client:
    def __init__(self, host="127.0.0.1", port=6060) -> None:
        self.__host = host
        self.__port = port

    def _send(self, service: str, function: str, parameters: dict):

        return requests.post(f"http://{self.__host}:{self.__port}/{service}/{function}/", json=parameters).json()

    def getDatabase(self, databaseName: str):
        from . import database

        return database.Database(self, databaseName)
