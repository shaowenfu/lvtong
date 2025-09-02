# -*- coding: utf-8 -*-
"""
聊天数据模型
- 定义聊天记录在MongoDB中的数据结构
- 与云数据库管理系统兼容
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from bson import ObjectId
from ..database import db_manager

class ChatMessage:
    """
    聊天消息模型
    用于MongoDB存储和查询聊天记录
    """
    COLLECTION_NAME = 'chat_messages'
    
    def __init__(self, user_id: str = None, content: str = None, role: str = None, 
                 message_id: str = None, timestamp: datetime = None, 
                 emotional_state: str = "neutral", tokens_used: int = 0, **kwargs):
        self.message_id = message_id or str(ObjectId())
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.role = role  # "user" or "assistant"
        self.emotional_state = emotional_state  # 情绪状态
        self.tokens_used = tokens_used  # 使用的token数量
        
        # MongoDB document ID
        self._id = kwargs.get('_id')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB storage"""
        data = {
            "message_id": self.message_id,
            "user_id": self.user_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "role": self.role,
            "emotional_state": self.emotional_state,
            "tokens_used": self.tokens_used
        }
        
        if self._id:
            data['_id'] = self._id
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """
        Create ChatMessage object from dictionary
        """
        return cls(**data)
    
    def save(self) -> str:
        """
        Save message to database
        Returns: document ID
        """
        data = self.to_dict()
        
        if self._id:
            # Update existing message
            db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                data
            )
            return str(self._id)
        else:
            # Create new message
            self._id = db_manager.create_one(self.COLLECTION_NAME, data)
            return self._id
    
    @classmethod
    def find_by_user(cls, user_id: str, limit: int = 50) -> List['ChatMessage']:
        """
        Find messages by user ID
        """
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME,
            {'user_id': user_id},
            limit=limit,
            sort=[('timestamp', -1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    @classmethod
    def find_by_session(cls, session_id: str, limit: int = 50) -> List['ChatMessage']:
        """
        Find messages by session ID
        """
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME,
            {'session_id': session_id},
            limit=limit,
            sort=[('timestamp', 1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    @classmethod
    def get_recent_messages(cls, user_id: str, hours: int = 24) -> List['ChatMessage']:
        """
        Get recent messages within specified hours
        """
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME,
            {
                'user_id': user_id,
                'timestamp': {'$gte': cutoff_time}
            },
            sort=[('timestamp', 1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    def to_openai_format(self) -> Dict[str, str]:
        """Convert to OpenAI API format"""
        return {
            "role": self.role,
            "content": self.content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create ChatMessage from dictionary"""
        return cls(
            message_id=str(data.get("_id", "")),
            user_id=data.get("user_id", ""),
            content=data.get("content", ""),
            timestamp=data.get("timestamp", datetime.now()),
            role=data.get("role", "user"),
            emotional_state=data.get("emotional_state", "neutral"),
            tokens_used=data.get("tokens_used", 0)
        )

class ChatSession:
    """
    聊天会话模型
    用于管理用户的聊天会话
    """
    COLLECTION_NAME = 'chat_sessions'
    
    def __init__(self, user_id: str = None, session_id: str = None, 
                 created_at: datetime = None, last_active: datetime = None, 
                 message_count: int = 0, **kwargs):
        self.session_id = session_id or str(ObjectId())
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
        self.last_active = last_active or datetime.now()
        self.message_count = message_count
        
        # MongoDB document ID
        self._id = kwargs.get('_id')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB storage"""
        data = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "message_count": self.message_count
        }
        
        if self._id:
            data['_id'] = self._id
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatSession':
        """
        Create ChatSession object from dictionary
        """
        return cls(**data)
    
    def save(self) -> str:
        """
        Save session to database
        Returns: document ID
        """
        data = self.to_dict()
        
        if self._id:
            # Update existing session
            db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                data
            )
            return str(self._id)
        else:
            # Create new session
            self._id = db_manager.create_one(self.COLLECTION_NAME, data)
            return self._id
    
    @classmethod
    def find_by_user(cls, user_id: str, limit: int = 10) -> List['ChatSession']:
        """
        Find sessions by user ID
        """
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME,
            {'user_id': user_id},
            limit=limit,
            sort=[('last_active', -1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    @classmethod
    def find_by_session_id(cls, session_id: str) -> Optional['ChatSession']:
        """
        Find session by session ID
        """
        data = db_manager.find_one(cls.COLLECTION_NAME, {'session_id': session_id})
        return cls.from_dict(data) if data else None
    
    def update_activity(self) -> bool:
        """
        Update last active time
        """
        self.last_active = datetime.now()
        
        if self._id:
            return db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                {'last_active': self.last_active}
            )
        return False
    
    def increment_message_count(self) -> bool:
        """
        Increment message count
        """
        self.message_count += 1
        self.last_active = datetime.now()
        
        if self._id:
            return db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                {
                    'message_count': self.message_count,
                    'last_active': self.last_active
                }
            )
        return False
