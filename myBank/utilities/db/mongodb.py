from pymongo import MongoClient


class MongoDB:
    def __init__(self, host: str = 'localhost', port: int = 27017, database: str = 'myBank'):
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[database]  # Replace 'myBank' with your database name

    def change_database(self, db_name: str):
        """ Changes the current database to the specified one """
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        """ Returns a collection from the MongoDB database """
        return self.db[collection_name]

    def insert_document(self, collection_name: str, document: list[dict]):
        collection = self.get_collection(collection_name)
        result = collection.insert_many(document)
        return result.inserted_ids

    def find_documents(self, collection_name: str, query: dict = {}):
        """ Finds documents in a collection based on the query """
        collection = self.get_collection(collection_name)
        return collection.find(query)

    def close(self):
        """ Closes the MongoDB connection """
        self.client.close()
