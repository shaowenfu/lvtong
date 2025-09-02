# -*- coding: utf-8 -*-
"""
心理分析报告数据模型
- 定义报告在MongoDB中的数据结构
- 与云数据库管理系统兼容
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from bson import ObjectId
from ..database import db_manager

class Report:
    """
    报告模型
    心理分析报告的数据模型
    """
    COLLECTION_NAME = 'reports'
    
    def __init__(self, report_id: str = None, user_id: str = None, 
                 content: Dict[str, Any] = None, created_at: datetime = None,
                 report_type: str = "psychological_analysis", status: str = "completed",
                 **kwargs):
        self.report_id = report_id or str(ObjectId())
        self.user_id = user_id
        self.content = content or {}  # 报告内容（dict格式）
        self.created_at = created_at or datetime.now()
        self.report_type = report_type  # 报告类型
        self.status = status  # 报告状态：pending, processing, completed, failed
        self.updated_at = kwargs.get('updated_at', datetime.now())
        
        # MongoDB document ID
        self._id = kwargs.get('_id')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert report object to dictionary for database storage
        """
        data = {
            'report_id': self.report_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at,
            'report_type': self.report_type,
            'status': self.status,
            'updated_at': self.updated_at
        }
        
        if self._id:
            data['_id'] = self._id
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Report':
        """
        Create Report object from dictionary
        """
        return cls(**data)
    
    def save(self) -> str:
        """
        Save report to database
        Returns: document ID
        """
        data = self.to_dict()
        
        if self._id:
            # Update existing report
            data['updated_at'] = datetime.now()
            db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                data
            )
            return str(self._id)
        else:
            # Create new report
            self._id = db_manager.create_one(self.COLLECTION_NAME, data)
            return self._id
    
    @classmethod
    def find_by_user(cls, user_id: str, limit: int = 10) -> List['Report']:
        """
        Find reports by user ID
        """
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME,
            {'user_id': user_id},
            limit=limit,
            sort=[('created_at', -1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    @classmethod
    def find_by_id(cls, report_id: str) -> Optional['Report']:
        """
        Find report by report ID
        """
        data = db_manager.find_one(cls.COLLECTION_NAME, {'report_id': report_id})
        return cls.from_dict(data) if data else None
    
    @classmethod
    def find_by_type(cls, report_type: str, limit: int = 50) -> List['Report']:
        """
        Find reports by type
        """
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME,
            {'report_type': report_type},
            limit=limit,
            sort=[('created_at', -1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    def update_status(self, new_status: str) -> bool:
        """
        Update report status
        """
        self.status = new_status
        self.updated_at = datetime.now()
        
        if self._id:
            return db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                {
                    'status': new_status,
                    'updated_at': self.updated_at
                }
            )
        return False
    
    def update_content(self, new_content: Dict[str, Any]) -> bool:
        """
        Update report content
        """
        self.content = new_content
        self.updated_at = datetime.now()
        
        if self._id:
            return db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                {
                    'content': new_content,
                    'updated_at': self.updated_at
                }
            )
        return False
    
    def delete(self) -> bool:
        """
        Delete report from database
        """
        if self._id:
            return db_manager.delete_one(self.COLLECTION_NAME, {'_id': self._id})
        return False
