import pymongo

class MongoDBHandler:
    def __init__(self, connection_string):
        self.client = pymongo.MongoClient(connection_string)
    
    def insert_document(self, document_dict, db_name="taskAnalysisDB", collection_name="tasks"):
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.insert_one(document_dict)
        return result
    
    def query_documents(self, query_dict=None, db_name="taskAnalysisDB", collection_name="tasks", projection=None, limit=None):
        db = self.client[db_name]
        collection = db[collection_name]
        cursor = collection.find(query_dict or {}, projection or {})
        if limit:
            cursor = cursor.limit(limit)
        return cursor
    
    def update_document(self, document_id, field_name, new_value, db_name="taskAnalysisDB", collection_name="tasks"):
        from bson import ObjectId
        if isinstance(document_id, str):
            document_id = ObjectId(document_id)
        
        db = self.client[db_name]
        collection = db[collection_name]
        filter_query = {"_id": document_id}
        update_query = {"$set": {field_name: new_value}}
        result = collection.update_one(filter_query, update_query)
        return result
    
    def close(self):
        self.client.close()