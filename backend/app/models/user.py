# -*- coding: utf-8 -*-
"""
用户数据模型
- 定义用户在MongoDB中的数据结构
"""

# 示例用户模型（可根据实际需求扩展字段）
class User:
    """
    用户模型
    TODO: 根据实际业务需求完善用户字段和方法
    """
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

# TODO: 可根据需要添加更多字段，如注册时间、用户状态等
