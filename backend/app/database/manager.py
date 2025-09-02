# -*- coding: utf-8 -*-
"""
Simple Database Manager
- Provides basic CRUD operations for MongoDB
- Simple and efficient database operations
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from ..config.database import db_config

class DatabaseManager:
    """
    Simple database manager for basic CRUD operations
    """
    
    def __init__(self):
        self.db = db_config.get_database()
    
    def get_collection(self, collection_name: str) -> Collection:
        """
        Get MongoDB collection
        """
        return self.db[collection_name]
    
    # Basic CRUD Operations
    
    def create_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        Create a single document
        Returns: document ID
        """
        try:
            # Add timestamp if not exists
            if 'created_at' not in document:
                document['created_at'] = datetime.now()
            
            collection = self.get_collection(collection_name)
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to create document: {e}")
    
    def create_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Create multiple documents
        Returns: list of document IDs
        """
        try:
            # Add timestamp to all documents
            for doc in documents:
                if 'created_at' not in doc:
                    doc['created_at'] = datetime.now()
            
            collection = self.get_collection(collection_name)
            result = collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except PyMongoError as e:
            raise Exception(f"Failed to create documents: {e}")
    
    def find_one(self, collection_name: str, filter_dict: Dict[str, Any] = None, 
                 projection: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Find a single document
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Handle ObjectId conversion
            if filter_dict and '_id' in filter_dict:
                if isinstance(filter_dict['_id'], str):
                    filter_dict['_id'] = ObjectId(filter_dict['_id'])
            
            result = collection.find_one(filter_dict or {}, projection)
            
            # Convert ObjectId to string for JSON serialization
            if result and '_id' in result:
                result['_id'] = str(result['_id'])
            
            return result
        except PyMongoError as e:
            raise Exception(f"Failed to find document: {e}")
    
    def find_many(self, collection_name: str, filter_dict: Dict[str, Any] = None,
                  projection: Dict[str, Any] = None, limit: int = None, 
                  sort: List[tuple] = None) -> List[Dict[str, Any]]:
        """
        Find multiple documents
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Handle ObjectId conversion in filter
            if filter_dict and '_id' in filter_dict:
                if isinstance(filter_dict['_id'], str):
                    filter_dict['_id'] = ObjectId(filter_dict['_id'])
            
            cursor = collection.find(filter_dict or {}, projection)
            
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
            
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for result in results:
                if '_id' in result:
                    result['_id'] = str(result['_id'])
            
            return results
        except PyMongoError as e:
            raise Exception(f"Failed to find documents: {e}")
    
    def update_one(self, collection_name: str, filter_dict: Dict[str, Any], 
                   update_dict: Dict[str, Any], upsert: bool = False) -> bool:
        """
        Update a single document
        Returns: True if document was modified
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Handle ObjectId conversion
            if '_id' in filter_dict:
                if isinstance(filter_dict['_id'], str):
                    filter_dict['_id'] = ObjectId(filter_dict['_id'])
            
            # Add update timestamp
            if '$set' not in update_dict:
                update_dict = {'$set': update_dict}
            
            update_dict['$set']['updated_at'] = datetime.now()
            
            result = collection.update_one(filter_dict, update_dict, upsert=upsert)
            return result.modified_count > 0 or result.upserted_id is not None
        except PyMongoError as e:
            raise Exception(f"Failed to update document: {e}")
    
    def update_many(self, collection_name: str, filter_dict: Dict[str, Any], 
                    update_dict: Dict[str, Any]) -> int:
        """
        Update multiple documents
        Returns: number of modified documents
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Add update timestamp
            if '$set' not in update_dict:
                update_dict = {'$set': update_dict}
            
            update_dict['$set']['updated_at'] = datetime.now()
            
            result = collection.update_many(filter_dict, update_dict)
            return result.modified_count
        except PyMongoError as e:
            raise Exception(f"Failed to update documents: {e}")
    
    def delete_one(self, collection_name: str, filter_dict: Dict[str, Any]) -> bool:
        """
        Delete a single document
        Returns: True if document was deleted
        """
        try:
            collection = self.get_collection(collection_name)
            
            # Handle ObjectId conversion
            if '_id' in filter_dict:
                if isinstance(filter_dict['_id'], str):
                    filter_dict['_id'] = ObjectId(filter_dict['_id'])
            
            result = collection.delete_one(filter_dict)
            return result.deleted_count > 0
        except PyMongoError as e:
            raise Exception(f"Failed to delete document: {e}")
    
    def delete_many(self, collection_name: str, filter_dict: Dict[str, Any]) -> int:
        """
        Delete multiple documents
        Returns: number of deleted documents
        """
        try:
            collection = self.get_collection(collection_name)
            result = collection.delete_many(filter_dict)
            return result.deleted_count
        except PyMongoError as e:
            raise Exception(f"Failed to delete documents: {e}")
    
    def count_documents(self, collection_name: str, filter_dict: Dict[str, Any] = None) -> int:
        """
        Count documents in collection
        """
        try:
            collection = self.get_collection(collection_name)
            return collection.count_documents(filter_dict or {})
        except PyMongoError as e:
            raise Exception(f"Failed to count documents: {e}")
    
    def aggregate(self, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute aggregation pipeline
        """
        try:
            collection = self.get_collection(collection_name)
            results = list(collection.aggregate(pipeline))
            
            # Convert ObjectId to string
            for result in results:
                if '_id' in result and isinstance(result['_id'], ObjectId):
                    result['_id'] = str(result['_id'])
            
            return results
        except PyMongoError as e:
            raise Exception(f"Failed to execute aggregation: {e}")

# Global database manager instance
db_manager = DatabaseManager()