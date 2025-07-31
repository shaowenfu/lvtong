# -*- coding: utf-8 -*-
"""
聊天服务
- 封装AI聊天、聊天历史等业务逻辑
- 支持念念AI人设
"""

from typing import Generator, Dict, Any, Optional
from .openai_service import OpenAIService
from ..config.persona_config import NianNianPersona
import random
import re
from datetime import datetime

class ChatService:
    """
    聊天服务类
    处理AI消息、历史记录查询等业务逻辑
    支持念念AI人设的情感陪伴功能
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.persona = NianNianPersona()
    
    def _analyze_emotion(self, message: str) -> str:
        """简单的情绪分析"""
        sad_keywords = ["难过", "伤心", "痛苦", "失落", "沮丧", "哭", "眼泪"]
        anxious_keywords = ["焦虑", "紧张", "担心", "害怕", "不安", "压力"]
        happy_keywords = ["开心", "高兴", "快乐", "兴奋", "愉快", "满足"]
        lonely_keywords = ["孤独", "寂寞", "一个人", "没人", "独自", "空虚"]
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in sad_keywords):
            return "sad"
        elif any(keyword in message_lower for keyword in anxious_keywords):
            return "anxious"
        elif any(keyword in message_lower for keyword in happy_keywords):
            return "happy"
        elif any(keyword in message_lower for keyword in lonely_keywords):
            return "lonely"
        else:
            return "neutral"
    
    def _build_personalized_system_prompt(self, user_profile: Dict = None, emotional_state: str = "neutral", user_emotional_history: str = "neutral") -> str:
        """构建个性化的系统提示词"""
        base_prompt = self.persona.SYSTEM_PROMPT
        
        # 根据用户画像调整提示词
        if user_profile:
            profile_context = "\n\n## 用户信息：\n"
            if user_profile.get("age_range"):
                profile_context += f"- 年龄段: {user_profile['age_range']}\n"
            if user_profile.get("personality"):
                profile_context += f"- 性格特点: {user_profile['personality']}\n"
            if user_profile.get("communication_style"):
                profile_context += f"- 沟通偏好: {user_profile['communication_style']}\n"
            if user_profile.get("interests"):
                profile_context += f"- 兴趣爱好: {user_profile['interests']}\n"
            
            base_prompt += profile_context
        
        # 根据情绪状态调整回应方式
        if emotional_state != "neutral":
            emotion_context = f"\n\n## 当前用户情绪状态: {emotional_state}\n请特别关注用户的情绪，给予相应的情感支持和理解。"
            base_prompt += emotion_context
        
        # 如果用户历史情绪状态与当前不同，提供连续性关怀
        if user_emotional_history != "neutral" and user_emotional_history != emotional_state:
            continuity_context = f"\n\n## 情绪变化提醒: 用户之前的情绪状态是{user_emotional_history}，现在是{emotional_state}，请关注这种变化并给予适当的关怀。"
            base_prompt += continuity_context
            
        return base_prompt
    
    def process_message_stream(self, message: str, conversation_history: list = None, 
                             user_profile: Dict = None, user_id: str = None) -> Generator[str, None, None]:
        """处理用户消息，生成AI流式回复（念念人设版本）"""
        # 分析用户情绪
        emotional_state = self._analyze_emotion(message)
        
        # 获取用户历史情绪状态
        user_emotional_history = "neutral"
        if user_id:
            profile_result = self.get_user_profile(user_id)
            user_emotional_history = profile_result.get("emotional_state", "neutral")
        
        # 构建消息列表
        messages = []
        
        # 添加个性化系统消息
        system_message = self._build_personalized_system_prompt(user_profile, emotional_state, user_emotional_history)
        messages.append({"role": "system", "content": system_message})
        
        # 添加历史对话（如果有）
        if conversation_history:
            messages.extend(conversation_history)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": message})
        
        # 保存用户消息到数据库
        if user_id:
            self.save_message(user_id, message, "user", emotional_state)
        
        # 调用OpenAI服务进行流式对话
        try:
            full_response = ""
            for chunk in self.openai_service.chat_stream(messages):
                if chunk:
                    full_response += chunk
                    yield chunk
            
            # 保存完整的AI回复到数据库
            if user_id and full_response:
                self.save_message(user_id, full_response, "assistant", "neutral")
                
        except Exception as e:
            # 提供温暖的错误回应
            error_response = "抱歉，我现在有点不舒服，可能需要休息一下...不过不用担心，我很快就会好起来的～"
            if user_id:
                self.save_message(user_id, error_response, "assistant", "neutral")
            yield error_response
    
    def process_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理用户消息，生成AI回复（非流式，念念人设版本）"""
        try:
            message = data.get("message", "")
            if not message:
                return {"error": "Message is required", "status": "error"}
            
            user_id = data.get("user_id")
            user_profile = data.get("user_profile", {})
            conversation_history = data.get("history", [])
            
            # 分析用户情绪
            emotional_state = self._analyze_emotion(message)
            
            # 获取用户历史情绪状态
            user_emotional_history = "neutral"
            if user_id:
                profile_result = self.get_user_profile(user_id)
                user_emotional_history = profile_result.get("emotional_state", "neutral")
            
            # 构建消息列表
            messages = []
            system_message = self._build_personalized_system_prompt(user_profile, emotional_state, user_emotional_history)
            messages.append({"role": "system", "content": system_message})
            
            # 添加历史对话
            if conversation_history:
                messages.extend(conversation_history)
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": message})
            
            # 调用OpenAI服务
            response, tokens = self.openai_service.chat(messages)
            
            if response:
                # 保存用户消息到数据库
                if user_id:
                    self.save_message(user_id, message, "user", emotional_state)
                    # 保存AI回复到数据库
                    self.save_message(user_id, response, "assistant", "neutral", tokens)
                
                return {
                    "response": response,
                    "tokens_used": tokens,
                    "emotional_state": emotional_state,
                    "persona": self.persona.NAME,
                    "status": "success"
                }
            else:
                return {
                    "error": "抱歉，我现在有点不舒服，可能需要休息一下...",
                    "status": "error"
                }
                
        except Exception as e:
            return {
                "error": "抱歉，出现了一些技术问题，但我会努力解决的～",
                "status": "error"
            }
    
    def get_greeting(self, time_period: str = "general") -> str:
        """获取问候语"""
        greetings = self.persona.GREETINGS.get(time_period, ["你好呀～我是念念，很高兴见到你～"])
        return random.choice(greetings)
    
    def get_emotional_response(self, emotion: str) -> str:
        """获取情绪回应"""
        responses = self.persona.EMOTIONAL_RESPONSES.get(emotion, [])
        if responses:
            return random.choice(responses)
        return "我能感受到你现在的情绪...无论如何，我都会陪着你的～"
    
    def get_profiling_question(self) -> str:
        """获取用户画像问题"""
        return random.choice(self.persona.PROFILING_QUESTIONS)
    
    def get_history(self, user_id: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get user chat history from MongoDB
        
        Args:
            user_id: User ID to query history for
            limit: Maximum number of messages to return (default: 20)
            
        Returns:
            Dict containing chat history and metadata
        """
        try:
            from ..extensions import mongo
            from ..models.chat import ChatMessage
            
            # Query messages from MongoDB, sorted by timestamp (newest first)
            messages_cursor = mongo.db.chat_messages.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit)
            
            # Convert to list and reverse to get chronological order
            messages_data = list(messages_cursor)
            messages_data.reverse()  # Oldest first for conversation context
            
            # Convert to OpenAI format for API consumption
            conversation_history = []
            for msg_data in messages_data:
                chat_msg = ChatMessage.from_dict(msg_data)
                conversation_history.append(chat_msg.to_openai_format())
            
            return {
                "history": conversation_history,
                "user_id": user_id,
                "message_count": len(conversation_history),
                "status": "success"
            }
            
        except Exception as e:
            # Log error and return empty history as fallback
            print(f"Error fetching chat history for user {user_id}: {str(e)}")
            return {
                "history": [],
                "user_id": user_id,
                "message_count": 0,
                "status": "success",
                "error": f"Failed to fetch history: {str(e)}"
            }
    
    def save_message(self, user_id: str, content: str, role: str, 
                    emotional_state: str = "neutral", tokens_used: int = 0) -> bool:
        """
        Save chat message to MongoDB
        
        Args:
            user_id: User ID
            content: Message content
            role: Message role ("user" or "assistant")
            emotional_state: Detected emotional state
            tokens_used: Number of tokens used
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            from ..extensions import mongo
            from ..models.chat import ChatMessage
            
            # Create chat message object
            chat_msg = ChatMessage(
                user_id=user_id,
                content=content,
                role=role,
                emotional_state=emotional_state,
                tokens_used=tokens_used
            )
            
            # Save to MongoDB
            result = mongo.db.chat_messages.insert_one(chat_msg.to_dict())
            
            # Update user's last active time and emotional state (for user messages)
            update_data = {"last_active": datetime.now()}
            if role == "user" and emotional_state != "neutral":
                update_data["emotional_state"] = emotional_state
            
            mongo.db.users.update_one(
                {"user_id": user_id},
                {"$set": update_data},
                upsert=True
            )
            
            return result.inserted_id is not None
            
        except Exception as e:
            print(f"Error saving message for user {user_id}: {str(e)}")
            return False
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile from MongoDB
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing user profile data
        """
        try:
            from ..extensions import mongo
            
            # Query user from MongoDB
            user_data = mongo.db.users.find_one({"user_id": user_id})
            
            if user_data:
                return {
                    "persona_profile": user_data.get("persona_profile", {}),
                    "persona_preferences": user_data.get("persona_preferences", {}),
                    "emotional_state": user_data.get("emotional_state", "neutral"),
                    "status": "success"
                }
            else:
                # Return default profile for new users
                return {
                    "persona_profile": {},
                    "persona_preferences": {},
                    "emotional_state": "neutral",
                    "status": "success",
                    "is_new_user": True
                }
                
        except Exception as e:
            print(f"Error fetching user profile for user {user_id}: {str(e)}")
            return {
                "persona_profile": {},
                "persona_preferences": {},
                "emotional_state": "neutral",
                "status": "error",
                "error": f"Failed to fetch profile: {str(e)}"
            }
    
    def clear_history(self, user_id: str) -> Dict[str, Any]:
        """
        Clear user's chat history
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with operation result
        """
        try:
            from ..extensions import mongo
            
            # Delete all messages for the user
            result = mongo.db.chat_messages.delete_many({"user_id": user_id})
            
            return {
                "deleted_count": result.deleted_count,
                "user_id": user_id,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to clear history: {str(e)}",
                "user_id": user_id,
                "status": "error"
            }

# TODO: 可根据需求扩展更多方法，如多模态对话、主动关怀推送等
