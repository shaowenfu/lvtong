# -*- coding: utf-8 -*-
"""
用户数据模型
- 定义用户在MongoDB中的数据结构
- 与云数据库管理系统兼容
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from ..database import db_manager

class User:
    """
    用户模型
    包含用户基础信息和AI人设相关配置
    """
    COLLECTION_NAME = 'users'
    
    def __init__(self, user_id: str = None, username: str = None, email: str = None, **kwargs):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = kwargs.get('created_at', datetime.now())
        
        # AI人设相关字段
        self.persona_profile = kwargs.get('persona_profile', {})  # 用户画像信息 
        self.persona_preferences = kwargs.get('persona_preferences', {})  # 个性化偏好
        self.emotional_state = kwargs.get('emotional_state', "neutral")  # 当前情绪状态
        self.interaction_history = kwargs.get('interaction_history', [])  # 交互历史摘要
        self.last_active = kwargs.get('last_active', datetime.now())  # 最后活跃时间
        
        # MongoDB document ID
        self._id = kwargs.get('_id')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user object to dictionary for database storage
        """
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'persona_profile': self.persona_profile,
            'persona_preferences': self.persona_preferences,
            'emotional_state': self.emotional_state,
            'interaction_history': self.interaction_history,
            'last_active': self.last_active
        }
        
        if self._id:
            data['_id'] = self._id
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create user object from dictionary
        """
        return cls(**data)
    
    def save(self) -> str:
        """
        Save user to database
        Returns: document ID
        """
        data = self.to_dict()
        
        if self._id:
            # Update existing user
            db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                data
            )
            return str(self._id)
        else:
            # Create new user
            self._id = db_manager.create_one(self.COLLECTION_NAME, data)
            return self._id
    
    @classmethod
    def find_by_id(cls, user_id: str) -> Optional['User']:
        """
        Find user by user_id
        """
        data = db_manager.find_one(cls.COLLECTION_NAME, {'user_id': user_id})
        return cls.from_dict(data) if data else None
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """
        Find user by email
        """
        data = db_manager.find_one(cls.COLLECTION_NAME, {'email': email})
        return cls.from_dict(data) if data else None
    
    @classmethod
    def find_all(cls, limit: int = None) -> List['User']:
        """
        Find all users
        """
        data_list = db_manager.find_many(
            cls.COLLECTION_NAME, 
            limit=limit,
            sort=[('created_at', -1)]
        )
        return [cls.from_dict(data) for data in data_list]
    
    def update_emotional_state(self, new_state: str) -> bool:
        """
        Update user's emotional state
        """
        self.emotional_state = new_state
        self.last_active = datetime.now()
        
        if self._id:
            return db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                {
                    'emotional_state': new_state,
                    'last_active': self.last_active
                }
            )
        return False
    
    def add_interaction(self, interaction_data: Dict[str, Any]) -> bool:
        """
        Add interaction to history
        """
        interaction_data['timestamp'] = datetime.now()
        self.interaction_history.append(interaction_data)
        self.last_active = datetime.now()
        
        # Keep only last 50 interactions
        if len(self.interaction_history) > 50:
            self.interaction_history = self.interaction_history[-50:]
        
        if self._id:
            return db_manager.update_one(
                self.COLLECTION_NAME,
                {'_id': self._id},
                {
                    'interaction_history': self.interaction_history,
                    'last_active': self.last_active
                }
            )
        return False
    
    def delete(self) -> bool:
        """
        Delete user from database
        """
        if self._id:
            return db_manager.delete_one(self.COLLECTION_NAME, {'_id': self._id})
        return False
        
    def update_persona_profile(self, profile_data: Dict):
        """更新用户画像信息"""
        self.persona_profile.update(profile_data)
        
    def update_emotional_state(self, emotion: str):
        """更新情绪状态"""
        self.emotional_state = emotion
        self.last_active = datetime.now()
        
    def add_interaction_summary(self, summary: str):
        """添加交互摘要"""
        self.interaction_history.append({
            "timestamp": datetime.now(),
            "summary": summary
        })
        # 保持最近20条记录
        if len(self.interaction_history) > 20:
            self.interaction_history = self.interaction_history[-20:]
            
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "persona_profile": self.persona_profile,
            "persona_preferences": self.persona_preferences,
            "emotional_state": self.emotional_state,
            "interaction_history": self.interaction_history,
            "last_active": self.last_active
        }
