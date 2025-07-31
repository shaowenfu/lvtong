# -*- coding: utf-8 -*-
"""
心理分析报告数据模型
- 定义报告在MongoDB中的数据结构
"""

# 示例报告模型（可根据实际需求扩展字段）
class Report:
    """
    报告模型
    TODO: 根据实际业务需求完善报告字段和方法
    """
    def __init__(self, report_id, user_id, content, created_at):
        self.report_id = report_id
        self.user_id = user_id
        self.content = content  # 报告内容（可为dict或json）
        self.created_at = created_at

# TODO: 可根据需要添加更多字段，如报告状态、更新时间等
