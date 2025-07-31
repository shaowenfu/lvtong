# -*- coding: utf-8 -*-
"""
用户数据模型
- 定义用户在MongoDB中的数据结构
"""

from datetime import datetime
from typing import Dict, List, Optional

class User:
    """
    用户模型
    包含用户基础信息和AI人设相关配置
    """
    def __init__(self, user_id: str, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.created_at = datetime.now()
        
        # AI人设相关字段
        self.persona_profile = {}  # 用户画像信息 
        self.persona_preferences = {}  # 个性化偏好
        self.emotional_state = "neutral"  # 当前情绪状态
        self.interaction_history = []  # 交互历史摘要
        self.last_active = datetime.now()  # 最后活跃时间
        
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
