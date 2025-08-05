# -*- coding: utf-8 -*-
"""
聊天相关路由模块
- 提供AI聊天、聊天历史等接口
- 聊天接口简化：只需要请求头中的X-User-ID和请求体中的message
- 其他参数（历史记录、用户画像等）由后端自动处理
"""

from flask import Blueprint, request, jsonify, Response, stream_template
import json
from ..services.chat_service import ChatService

chat_bp = Blueprint("chat", __name__)
chat_service = ChatService()

def clean_message_content(message: str) -> str:
    """
    Clean message content by removing system prompt if present
    If the message contains the prompt ending marker, remove everything before and including it
    """
    prompt_ending = "注意聊天需要简短像朋友聊天一样不要长篇大论。"
    
    if prompt_ending in message:
        # Find the position after the prompt ending
        split_pos = message.find(prompt_ending) + len(prompt_ending)
        # Extract only the user message part (everything after the prompt)
        cleaned_message = message[split_pos:].strip()
        return cleaned_message
    
    return message

@chat_bp.route("/message", methods=["POST"])
def chat_message():
    """
    AI聊天接口 - 流式输出
    接收用户消息，自动查找聊天历史，调用Azure OpenAI API，返回流式响应
    请求头: X-User-ID - 用户ID
    请求体: {"message": "用户消息"}
    """
    try:
        # 从请求头获取user_id
        user_id = request.headers.get('X-User-ID')
        if not user_id or not user_id.strip():
            return jsonify({"error": "X-User-ID header is required", "status": "error"}), 400
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        raw_message = data.get("message", "").strip()
        if not raw_message:
            return jsonify({"error": "Message is required", "status": "error"}), 400
        
        # Clean the message content to remove system prompt if present
        message = clean_message_content(raw_message)
        if not message:
            return jsonify({"error": "Message content is empty after cleaning", "status": "error"}), 400
        
        # 后端自动查找聊天历史
        history_result = chat_service.get_history(user_id)
        conversation_history = history_result.get("history", [])
        
        # 后端自动获取用户画像信息（从数据库或默认值）
        profile_result = chat_service.get_user_profile(user_id)
        user_profile = profile_result.get("persona_profile", {})
        
        # 定义流式响应生成器
        def generate_response():
            try:
                # 发送开始标记
                yield f"data: {json.dumps({'type': 'start', 'message': 'Response started'})}\n\n"
                
                # 流式生成AI回复
                for chunk in chat_service.process_message_stream(
                    message, 
                    conversation_history, 
                    user_profile, 
                    user_id
                ):
                    if chunk:
                        # 发送内容块
                        yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
                
                # 发送结束标记
                yield f"data: {json.dumps({'type': 'end', 'message': 'Response completed'})}\n\n"
                
            except Exception as e:
                # 发送错误信息
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
            
            # 发送完成标记
            yield "data: [DONE]\n\n"
        
        # 返回流式响应
        return Response(
            generate_response(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@chat_bp.route("/message/sync", methods=["POST"])
def chat_message_sync():
    """
    AI聊天接口 - 同步响应
    接收用户消息，自动查找聊天历史，调用Azure OpenAI API，返回完整响应
    请求头: X-User-ID - 用户ID
    请求体: {"message": "用户消息"}
    """
    try:
        # 从请求头获取user_id
        user_id = request.headers.get('X-User-ID')
        if not user_id or not user_id.strip():
            return jsonify({"error": "X-User-ID header is required", "status": "error"}), 400
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required", "status": "error"}), 400
        
        raw_message = data.get("message", "").strip()
        if not raw_message:
            return jsonify({"error": "Message is required", "status": "error"}), 400
        
        # Clean the message content to remove system prompt if present
        message = clean_message_content(raw_message)
        if not message:
            return jsonify({"error": "Message content is empty after cleaning", "status": "error"}), 400
        
        # 后端自动查找聊天历史
        history_result = chat_service.get_history(user_id)
        conversation_history = history_result.get("history", [])
        
        # 构建完整的数据对象传递给服务层
        complete_data = {
            "message": message,
            "user_id": user_id,
            "history": conversation_history,
            "user_profile": chat_service.get_user_profile(user_id).get("persona_profile", {})
        }
        
        # 调用chat_service处理消息
        result = chat_service.process_message(complete_data)
        
        if result.get("status") == "error":
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@chat_bp.route("/history", methods=["GET"])
def chat_history():
    """
    获取聊天历史接口
    从数据库获取用户聊天历史记录
    """
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required", "status": "error"}), 400
        
        # 调用chat_service获取历史记录
        result = chat_service.get_history(user_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

@chat_bp.route("/health", methods=["GET"])
def chat_health():
    """
    聊天服务健康检查接口
    检查OpenAI服务是否可用
    """
    try:
        # 检查OpenAI服务可用性
        available_models = chat_service.openai_service.get_available_models()
        
        return jsonify({
            "status": "healthy",
            "available_models": available_models,
            "service": "chat"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "service": "chat"
        }), 500

# TODO: 可根据需求添加更多聊天相关接口，如多模态对话、模式切换等
