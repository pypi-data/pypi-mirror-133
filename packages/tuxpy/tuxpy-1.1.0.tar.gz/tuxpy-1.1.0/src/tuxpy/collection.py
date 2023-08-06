from . import client


class Collection:

    __SERVICE_NAME = "collection"

    def __init__(self, client: client.Client, databaseName: str, collectionName: str) -> None:
        self.__client = client
        self.__databaseName = databaseName
        self.__collectionName = collectionName

    def getName(self) -> str:
        return self.__collectionName

    def setName(self, newCollectionName: str) -> dict:
        response = dict(self.__client._send(self.__SERVICE_NAME, "setName", {
                        "databaseName": self.__databaseName, "collectionName": self.__collectionName, "newCollectionName": newCollectionName}))

        if response.get("success"):
            self.__collectionName = newCollectionName

        return response

    def getAllObjects(self) -> list:
        return list(self.__client._send(self.__SERVICE_NAME, "getAllObjects", {"databaseName": self.__databaseName, "collectionName": self.__collectionName}))

    def findFromObjectId(self, objectId: str) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "findFromObjectId", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "objectId": objectId}))

    def findOne(self, query: dict) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "findOne", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "query": query}))

    def find(self, query: dict) -> list:
        return list(self.__client._send(self.__SERVICE_NAME, "find", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "query": query}))

    def insert(self, data: dict) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "insert", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "data": data}))

    def updateFromObjectId(self, objectId: str, updateData: dict) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "updateFromObjectId", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "objectId": objectId, "updateData": updateData}))

    def update(self, query: dict, updateData: dict) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "update", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "query": query, "updateData": updateData}))

    def deleteFromObjectId(self, objectId: str) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "deleteFromObjectId", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "objectId": objectId}))

    def delete(self, query: dict) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "delete", {"databaseName": self.__databaseName, "collectionName": self.__collectionName, "query": query}))

    def drop(self) -> dict:
        return dict(self.__client._send(self.__SERVICE_NAME, "drop", {"databaseName": self.__databaseName, "collectionName": self.__collectionName}))

    def __str__(self) -> str:
        return f"{self.__databaseName}.{self.__collectionName}"
