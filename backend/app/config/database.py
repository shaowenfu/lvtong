
# -*- coding: utf-8 -*-
"""
MongoDB Cloud Database Configuration
- Support environment variable based connection
- Simple and secure cloud database connection
"""

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Optional

class CloudDatabaseConfig:
    """
    Cloud MongoDB configuration and connection manager
    """
    
    def __init__(self):
        # Read MongoDB connection info from environment variables
        self.mongodb_uri = os.getenv('MONGODB_CLOUD_URI')
        self.mongodb_username = os.getenv('MONGODB_USERNAME')
        self.mongodb_password = os.getenv('MONGODB_PASSWORD')
        self.mongodb_cluster = os.getenv('MONGODB_CLUSTER')
        self.mongodb_database = os.getenv('MONGODB_DATABASE', 'lvtong')
        self.mongodb_app_name = os.getenv('MONGODB_APP_NAME', 'LvTong')
        
        # Fallback to local MongoDB if cloud config not available
        self.fallback_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/lvtong')
        
        self._client: Optional[MongoClient] = None
    
    def get_connection_uri(self) -> str:
        """
        Get MongoDB connection URI
        Priority: MONGODB_CLOUD_URI > constructed URI > fallback URI
        """
        if self.mongodb_uri:
            return self.mongodb_uri
        
        if self.mongodb_username and self.mongodb_password and self.mongodb_cluster:
            return f"mongodb+srv://{self.mongodb_username}:{self.mongodb_password}@{self.mongodb_cluster}/?retryWrites=true&w=majority&appName={self.mongodb_app_name}"
        
        return self.fallback_uri
    
    def get_client(self) -> MongoClient:
        """
        Get MongoDB client instance (singleton pattern)
        """
        if self._client is None:
            uri = self.get_connection_uri()
            try:
                if 'mongodb+srv://' in uri:
                    # Cloud MongoDB with SRV
                    self._client = MongoClient(uri, server_api=ServerApi('1'))
                else:
                    # Local MongoDB
                    self._client = MongoClient(uri)
                
                # Test connection
                self._client.admin.command('ping')
                print(f"Successfully connected to MongoDB: {self.mongodb_database}")
                
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise
        
        return self._client
    
    def get_database(self):
        """
        Get database instance
        """
        client = self.get_client()
        return client[self.mongodb_database]
    
    def close_connection(self):
        """
        Close MongoDB connection
        """
        if self._client:
            self._client.close()
            self._client = None

# Global database config instance
db_config = CloudDatabaseConfig()

# For backward compatibility
client = db_config.get_client()
database = db_config.get_database()