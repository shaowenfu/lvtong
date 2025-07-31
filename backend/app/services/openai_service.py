# -*- coding: utf-8 -*-
"""
OpenAI Azure API服务
- 封装与OpenAI Azure API的交互逻辑
"""

import os
import time
import requests
import json
from typing import List, Dict, Tuple, Optional, Generator

class OpenAIService:
    """
    OpenAI Azure服务类
    封装Azure OpenAI API调用，支持多模型和多种配置
    """
    
    def __init__(self):
        # Azure OpenAI API密钥映射（支持多个模型）
        self.AZURE_AI_API_KEY_MAP = {
            "4o": os.getenv("AZURE_AI_API_KEY_4O", ""),
            "gpt-4": os.getenv("AZURE_AI_API_KEY_GPT4", ""),
            "gpt-35-turbo": os.getenv("AZURE_AI_API_KEY_GPT35", "")
        }
        
        # Azure OpenAI 模型端点映射
        self.AZURE_AI_MODEL_ENDPOINT = {
            "4o": os.getenv("AZURE_AI_ENDPOINT_4O", ""),
            "gpt-4": os.getenv("AZURE_AI_ENDPOINT_GPT4", ""),
            "gpt-35-turbo": os.getenv("AZURE_AI_ENDPOINT_GPT35", "")
        }
        
        # 默认配置
        self.default_temperature = 0.7
        self.default_max_tokens = 2048
        self.default_top_p = 1
        self.default_model = "4o"
    
    def print_log(self, message: str):
        """
        打印日志信息
        TODO: 后续可以替换为更完善的日志系统
        """
        print(f"[OpenAI Service] {message}")
    
    def call_azure_gpt_with_messages(
        self, 
        message_list: List[Dict], 
        temperature: float = None,
        max_tokens: int = None,
        json_response: bool = False,
        model: str = None,
        top_p: float = None
    ) -> Tuple[Optional[str], int]:
        """
        调用Azure GPT模型进行对话
        
        Args:
            message_list: 消息列表，格式为 [{"role": "user", "content": "消息内容"}, ...]
            temperature: 温度参数，控制回复的随机性 (0-1)
            max_tokens: 最大token数
            json_response: 是否返回JSON格式
            model: 使用的模型名称
            top_p: top_p参数
            
        Returns:
            Tuple[回复内容, 使用的token数量]
        """
        # 使用默认值
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        model = model if model is not None else self.default_model
        top_p = top_p if top_p is not None else self.default_top_p
        
        # 验证模型是否支持
        if model not in self.AZURE_AI_API_KEY_MAP:
            self.print_log(f"不支持的模型: {model}")
            return None, 0
            
        # 获取API密钥和端点
        api_key = self.AZURE_AI_API_KEY_MAP[model]
        endpoint = self.AZURE_AI_MODEL_ENDPOINT[model]
        
        if not api_key or not endpoint:
            self.print_log(f"模型 {model} 的API密钥或端点未配置")
            return None, 0
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }
        
        # 设置响应格式
        response_format = {"type": "text"}  # 返回文本格式
        if json_response:
            response_format = {"type": "json_object"}
        
        # 构造请求体
        payload = {
            "messages": message_list,
            "temperature": temperature,
            "response_format": response_format,
            "top_p": top_p,
            "max_tokens": max_tokens
        }
        
        self.print_log(f"调用Azure OpenAI模型 {model}，消息数量: {len(message_list)}")
        
        start_time = time.time()  # 记录开始时间
        
        # 发送请求并处理响应
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # 检查请求是否成功
            
            res = response.json()
            
            end_time = time.time()  # 记录结束时间
            elapsed_time = end_time - start_time  # 计算执行时间
            self.print_log(f"Azure OpenAI API调用耗时 {elapsed_time:.2f} 秒")
            
            token = res["usage"]["total_tokens"]
            self.print_log(f"使用了 {token} 个tokens")
            
            return res["choices"][0]["message"]["content"], token
            
        except requests.RequestException as e:
            self.print_log(f"API请求失败: {e}")
            return None, 0
        except KeyError as e:
            self.print_log(f"响应格式错误: {e}")
            return None, 0
        except Exception as e:
            self.print_log(f"未知错误: {e}")
            return None, 0
    
    def chat(self, messages: List[Dict], **kwargs) -> Tuple[Optional[str], int]:
        """
        简化的聊天接口，兼容原有代码
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Returns:
            Tuple[回复内容, 使用的token数量]
        """
        return self.call_azure_gpt_with_messages(messages, **kwargs)
    
    def generate_single_response(
        self, 
        prompt: str, 
        system_message: str = None,
        **kwargs
    ) -> Tuple[Optional[str], int]:
        """
        生成单次回复的便捷方法
        
        Args:
            prompt: 用户输入
            system_message: 系统消息（可选）
            **kwargs: 其他参数
            
        Returns:
            Tuple[回复内容, 使用的token数量]
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        messages.append({"role": "user", "content": prompt})
        
        return self.call_azure_gpt_with_messages(messages, **kwargs)
    
    def is_model_available(self, model: str) -> bool:
        """
        检查指定模型是否可用
        
        Args:
            model: 模型名称
            
        Returns:
            bool: 模型是否可用
        """
        return (
            model in self.AZURE_AI_API_KEY_MAP and 
            bool(self.AZURE_AI_API_KEY_MAP[model]) and
            bool(self.AZURE_AI_MODEL_ENDPOINT.get(model))
        )
    
    def get_available_models(self) -> List[str]:
        """
        获取所有可用的模型列表
        
        Returns:
            List[str]: 可用模型列表
        """
        return [model for model in self.AZURE_AI_API_KEY_MAP.keys() if self.is_model_available(model)]
    
    def call_azure_gpt_stream(
        self, 
        message_list: List[Dict], 
        temperature: float = None,
        max_tokens: int = None,
        model: str = None,
        top_p: float = None
    ) -> Generator[str, None, None]:
        """
        调用Azure GPT模型进行流式对话
        
        Args:
            message_list: 消息列表，格式为 [{"role": "user", "content": "消息内容"}, ...]
            temperature: 温度参数，控制回复的随机性 (0-1)
            max_tokens: 最大token数
            model: 使用的模型名称
            top_p: top_p参数
            
        Yields:
            str: 流式返回的文本片段
        """
        # 使用默认值
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        model = model if model is not None else self.default_model
        top_p = top_p if top_p is not None else self.default_top_p
        
        # 验证模型是否支持
        if model not in self.AZURE_AI_API_KEY_MAP:
            self.print_log(f"Unsupported model: {model}")
            return
            
        # 获取API密钥和端点
        api_key = self.AZURE_AI_API_KEY_MAP[model]
        endpoint = self.AZURE_AI_MODEL_ENDPOINT[model]
        
        if not api_key or not endpoint:
            self.print_log(f"API key or endpoint not configured for model {model}")
            return
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }
        
        # 构造请求体，启用流式输出
        payload = {
            "messages": message_list,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        self.print_log(f"Calling Azure OpenAI model {model} with streaming, message count: {len(message_list)}")
        
        try:
            # 发送流式请求
            response = requests.post(endpoint, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            
            # 处理流式响应
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # 移除 'data: ' 前缀
                        
                        if data.strip() == '[DONE]':
                            break
                            
                        try:
                            json_data = json.loads(data)
                            if 'choices' in json_data and len(json_data['choices']) > 0:
                                delta = json_data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            continue
                            
        except requests.RequestException as e:
            self.print_log(f"API request failed: {e}")
            return
        except Exception as e:
            self.print_log(f"Unknown error: {e}")
            return
    
    def chat_stream(self, messages: List[Dict], **kwargs) -> Generator[str, None, None]:
        """
        简化的流式聊天接口
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Yields:
            str: 流式返回的文本片段
        """
        yield from self.call_azure_gpt_stream(messages, **kwargs)
