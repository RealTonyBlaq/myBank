from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId


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

    def insert_documents(self, collection_name: str, documents: list[dict]):
        collection = self.get_collection(collection_name)
        for doc in documents:
            doc.setdefault("timestamp",
                           {'created_at': datetime.now(),
                            'updated_at': datetime.now()})
        result = collection.insert_many(documents)
        return result.inserted_ids

    def doc_exists(self, collection_name: str, query: dict) -> bool:
        """ Checks if a document exists in a collection """
        collection = self.get_collection(collection_name)
        result = collection.find_one(query)
        return False if result is None else True

    def find_documents(self, collection_name: str, query: dict = {}):
        """ Finds documents in a collection based on the query """
        collection = self.get_collection(collection_name)
        return [doc for doc in collection.find(query)]

    def find_by_id(self, collection_name: str, doc_id: str):
        """ Finds a document by its ID """
        collection = self.get_collection(collection_name)
        try:
            id = ObjectId(doc_id)
            return collection.find_one({"_id": id})
        except (InvalidId, TypeError):
            print(f"Invalid ID {doc_id}")
            return None

    def update_document(self, collection_name: str, doc_id: str, update_data: dict):
        """ Updates a document in a collection by its ID """
        collection = self.get_collection(collection_name)
        try:
            id = ObjectId(doc_id)
        except (InvalidId, TypeError):
            print(f"Invalid ID: {doc_id}")
            return 0

        result = collection.update_one({"_id": id}, {"$set": update_data,
                                                     "$set": {"timestamp.updated_at": datetime.now()}})
        return result.modified_count

    def delete_doc_by_id(self, collection_name: str, doc_id: str):
        """ Deletes a document from a collection by its ID """
        collection = self.get_collection(collection_name)
        try:
            id = ObjectId(doc_id)
        except (InvalidId, TypeError):
            print(f"Invalid ID: {doc_id}")
            return 0

        result = collection.delete_one({"_id": id})
        return result.deleted_count

    def close(self):
        """ Closes the MongoDB connection """
        self.client.close()
