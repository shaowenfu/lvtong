# -*- coding: utf-8 -*-
"""
报告相关路由模块
- 提供报告生成、更新等接口
"""

from flask import Blueprint, request, jsonify
import re
import json
import csv
import os
from ..services.openai_service import OpenAIService
from ..services.report_service import ReportService

report_bp = Blueprint("report", __name__)
report_service = ReportService()

@report_bp.route("/overview", methods=["POST"])
def generate_overview_report():
    """
    生成心灵总览 (Mind Overview)报告的接口
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        # TODO: 实现心灵总览报告生成逻辑
        result = report_service.generate_overview_report(data)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@report_bp.route("/big_five", methods=["POST"])
def generate_big_five_report():
    """
    生成大五模型 (The Big Five)报告的接口
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        # 处理用户答案
        answers = data.get('answers', [])
        if not answers:
            return jsonify({"error": "Answers are required", "status": "error"}), 400
        
        result = report_service.generate_big_five_report(answers)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@report_bp.route("/core_values", methods=["POST"])
def generate_core_values_report():
    """
    生成价值观报告的接口
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        # 处理用户答案
        answers = data.get('answers', [])
        if not answers:
            return jsonify({"error": "Answers are required", "status": "error"}), 400
        
        result = report_service.generate_core_values_report(answers)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@report_bp.route("/mood", methods=["POST"])
def generate_mood_report():
    """
    生成情绪晴雨表 (Mood Barometer)报告的接口
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        # TODO: 实现情绪晴雨表报告生成逻辑
        result = report_service.generate_mood_report(data)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@report_bp.route("/growth_journal", methods=["POST"])
def update_growth_journal():
    """
    成长印记 (Growth Journal)报告的接口
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        # TODO: 实现成长印记报告更新逻辑
        result = report_service.update_growth_journal(data)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@report_bp.route("/holistic", methods=["POST"])
def generate_holistic_report():
    """
    生成综合心理画像报告的接口
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        core_values_data = data.get('core_values_data')
        big_five_data = data.get('big_five_data')
        
        if not core_values_data or not big_five_data:
            return jsonify({
                "error": "Both core_values_data and big_five_data are required", 
                "status": "error"
            }), 400
        
        result = report_service.generate_holistic_report(core_values_data, big_five_data)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

# TODO: 可根据需求添加更多报告相关接口，如获取历史报告、报告详情等
