# -*- coding: utf-8 -*-
"""
聊天数据模型
- 定义聊天记录在MongoDB中的数据结构
"""

# 示例聊天模型（可根据实际需求扩展字段）
class ChatMessage:
    """
    聊天消息模型
    TODO: 根据实际业务需求完善聊天消息字段和方法
    """
    def __init__(self, message_id, user_id, content, timestamp, role):
        self.message_id = message_id
        self.user_id = user_id
        self.content = content  # 消息内容
        self.timestamp = timestamp  # 消息时间
        self.role = role  # 角色（如user/ai）

# TODO: 可根据需要添加更多字段，如消息类型、多模态内容等
