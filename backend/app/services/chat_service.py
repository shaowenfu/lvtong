# -*- coding: utf-8 -*-
"""
聊天服务
- 封装AI聊天、聊天历史等业务逻辑
"""

from typing import Generator, Dict, Any
from .openai_service import OpenAIService

class ChatService:
    """
    聊天服务类
    处理AI消息、历史记录查询等业务逻辑
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
    
    def process_message_stream(self, message: str, conversation_history: list = None) -> Generator[str, None, None]:
        """
        处理用户消息，生成AI流式回复
        
        Args:
            message: 用户输入的消息
            conversation_history: 对话历史记录（可选）
            
        Yields:
            str: AI回复的文本片段
        """
        # 构建消息列表
        messages = []
        
        # 添加系统消息
        system_message = "You are a helpful AI assistant. Please respond in a friendly and informative manner."
        messages.append({"role": "system", "content": system_message})
        
        # 添加历史对话（如果有）
        if conversation_history:
            messages.extend(conversation_history)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": message})
        
        # 调用OpenAI服务进行流式对话
        try:
            yield from self.openai_service.chat_stream(messages)
        except Exception as e:
            yield f"Error: Failed to generate response - {str(e)}"
    
    def process_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理用户消息，生成AI回复（非流式）
        
        Args:
            data: 包含用户消息的数据字典
            
        Returns:
            Dict: 包含AI回复的响应数据
        """
        try:
            message = data.get("message", "")
            if not message:
                return {"error": "Message is required", "status": "error"}
            
            conversation_history = data.get("history", [])
            
            # 构建消息列表
            messages = []
            system_message = "You are a helpful AI assistant. Please respond in a friendly and informative manner."
            messages.append({"role": "system", "content": system_message})
            
            # 添加历史对话
            if conversation_history:
                messages.extend(conversation_history)
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": message})
            
            # 调用OpenAI服务
            response, tokens = self.openai_service.chat(messages)
            
            if response:
                return {
                    "response": response,
                    "tokens_used": tokens,
                    "status": "success"
                }
            else:
                return {"error": "Failed to generate response", "status": "error"}
                
        except Exception as e:
            return {"error": f"Service error: {str(e)}", "status": "error"}

    def get_history(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户聊天历史
        TODO: 实现从MongoDB查询历史记录
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 包含聊天历史的响应数据
        """
        # 临时返回空历史，后续可以接入数据库
        return {
            "history": [],
            "user_id": user_id,
            "status": "success"
        }

# TODO: 可根据需求扩展更多方法，如多模态对话、模式切换等
