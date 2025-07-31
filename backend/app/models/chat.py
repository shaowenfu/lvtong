# -*- coding: utf-8 -*-
"""
聊天数据模型
- 定义聊天记录在MongoDB中的数据结构
"""

from datetime import datetime
from typing import Dict, Any
from bson import ObjectId

class ChatMessage:
    """
    聊天消息模型
    用于MongoDB存储和查询聊天记录
    """
    def __init__(self, user_id: str, content: str, role: str, 
                 message_id: str = None, timestamp: datetime = None, 
                 emotional_state: str = "neutral", tokens_used: int = 0):
        self.message_id = message_id or str(ObjectId())
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.role = role  # "user" or "assistant"
        self.emotional_state = emotional_state  # 情绪状态
        self.tokens_used = tokens_used  # 使用的token数量
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB storage"""
        return {
            "_id": self.message_id,
            "user_id": self.user_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "role": self.role,
            "emotional_state": self.emotional_state,
            "tokens_used": self.tokens_used
        }
    
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
    def __init__(self, user_id: str, session_id: str = None, 
                 created_at: datetime = None, last_active: datetime = None):
        self.session_id = session_id or str(ObjectId())
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
        self.last_active = last_active or datetime.now()
        self.message_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB storage"""
        return {
            "_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "message_count": self.message_count
        }
