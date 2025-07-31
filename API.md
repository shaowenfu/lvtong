# LvTong Backend API 文档

基于 **`routes`** 目录下的路由文件，为您生成完整的 API 文档。

## 基础信息

- **Base URL**: **http://localhost:5000**
- **Content-Type**: **application/json**
- **API 前缀**: **/api**

---

## 1. 聊天模块 (Chat API)

### 1.1 AI 聊天接口 - 流式输出

**接口**: **POST /api/chat/message**

**描述**: 接收用户消息，调用 Azure OpenAI API，返回流式响应

**请求参数**:

```
JSON
{
  "message": "你好，请介绍一下自己",
  "history": [
    {
      "role": "user",
      "content": "之前的对话内容"
    },
    {
      "role": "assistant",
      "content": "AI的回复内容"
    }
  ]
}

```

**响应格式**: Server-Sent Events (SSE)

```
PlainText

data: {"type": "start", "message":
"Response started"}
data: {"type": "content",
"content": "回复内容片段"}
data: {"type": "end", "message":
"Response completed"}
data: [DONE]

```

**cURL 命令**:

```
Bash
运行

curl -X POST http://localhost:5000/
api/chat/message \
  -H "Content-Type: application/
  json" \
  -d '{
    "message": "你好，请介绍一下自己",
    "history": []
  }'

```

### 1.2 AI 聊天接口 - 同步响应

**接口**: **POST /api/chat/message/sync**

**描述**: 接收用户消息，返回完整的同步响应

**请求参数**:

```
JSON

{
  "message": "你好，请介绍一下自己",
  "history": []
}

```

**响应示例**:

```
JSON

{
  "status": "success",
  "response": "你好！我是一个AI助手...
  ",
  "timestamp":
  "2024-01-01T12:00:00Z"
}

```

**cURL 命令**:

```
Bash
运行

curl -X POST http://localhost:5000/
api/chat/message/sync \
  -H "Content-Type: application/
  json" \
  -d '{
    "message": "你好，请介绍一下自己",
    "history": []
  }'

```

### 1.3 获取聊天历史

**接口**: **GET /api/chat/history**

**描述**: 从数据库获取用户聊天历史记录

**查询参数**:

- **user_id** (必需): 用户ID

**响应示例**:

```
JSON

{
  "status": "success",
  "history": [
    {
      "timestamp":
      "2024-01-01T12:00:00Z",
      "message": "用户消息",
      "response": "AI回复"
    }
  ]
}

```

**cURL 命令**:

```
Bash
运行
curl -X GET "http://localhost:5000/
api/chat/history?user_id=12345"

```

### 1.4 聊天服务健康检查

**接口**: **GET /api/chat/health**

**描述**: 检查 OpenAI 服务是否可用

**响应示例**:

```
JSON

{
  "status": "healthy",
  "available_models": ["gpt-4",
  "gpt-3.5-turbo"],
  "service": "chat"
}

```

**cURL 命令**:

```
Bash
运行
curl -X GET http://localhost:5000/
api/chat/health

```

---

## 2. 报告模块 (Report API)

### 2.1 生成心灵总览报告

**接口**: **POST /api/report/overview**

**描述**: 生成心灵总览 (Mind Overview) 报告

**请求参数**:

```
JSON
{
  "user_data": {
    "user_id": "12345",
    "assessment_data": {}
  }
}

```

**响应示例**:

```
JSON
{
  "status": "success",
  "report": {
    "overview": "心灵总览内容",
    "insights": ["洞察1", "洞察2"]
  }
}

```

**cURL 命令**:

```
Bash
运行
curl -X POST http://localhost:5000/
api/report/overview \
  -H "Content-Type: application/
  json" \
  -d '{
    "user_data": {
      "user_id": "12345",
      "assessment_data": {}
    }
  }'

```

### 2.2 生成大五模型报告

**接口**: **POST /api/report/big_five**

**描述**: 生成大五模型 (The Big Five) 人格测评报告

**请求参数**:

```
JSON
{
  "answers": [
    {
      "question_id": 1,
      "answer": 4,
      "dimension": "openness"
    },
    {
      "question_id": 2,
      "answer": 3,
      "dimension":
      "conscientiousness"
    }
  ]
}

```

**响应示例**:

```
JSON
{
  "status": "success",
  "report": {
    "openness": 75,
    "conscientiousness": 68,
    "extraversion": 82,
    "agreeableness": 71,
    "neuroticism": 45,
    "analysis": "详细分析内容"
  }
}

```

**cURL 命令**:

```
Bash
运行
curl -X POST http://localhost:5000/
api/report/big_five \
  -H "Content-Type: application/
  json" \
  -d '{
    "answers": [
      {"question_id": 1, "answer":
      4, "dimension": "openness"},
      {"question_id": 2, "answer":
      3, "dimension":
      "conscientiousness"}
    ]
  }'

```

### 2.3 生成价值观报告

**接口**: **POST /api/report/core_values**

**描述**: 生成个人核心价值观分析报告

**请求参数**:

```
JSON
{
  "answers": [
    {
      "value_category":
      "achievement",
      "importance_score": 8
    },
    {
      "value_category": "security",
      "importance_score": 6
    }
  ]
}

```

**响应示例**:

```
JSON
{
  "status": "success",
  "report": {
    "core_values": ["成就", "安全", "
    自主"],
    "value_profile": "价值观画像描述",
    "recommendations": ["建议1", "建
    议2"]
  }
}

```

**cURL 命令**:

```
Bash
运行
curl -X POST http://localhost:5000/
api/report/core_values \
  -H "Content-Type: application/
  json" \
  -d '{
    "answers": [
      {"value_category":
      "achievement",
      "importance_score": 8},
      {"value_category":
      "security",
      "importance_score": 6}
    ]
  }'

```

### 2.4 生成情绪晴雨表报告

**接口**: **POST /api/report/mood**

**描述**: 生成情绪晴雨表 (Mood Barometer) 报告

**请求参数**:

```
JSON

{
  "mood_data": {
    "current_mood": "happy",
    "mood_intensity": 7,
    "mood_triggers":
    ["work_success",
    "social_interaction"]
  }
}

```

**响应示例**:

```
JSON

{
  "status": "success",
  "report": {
    "mood_analysis": "情绪分析内容",
    "mood_trends": "情绪趋势",
    "suggestions": ["建议1", "建议2"]
  }
}

```

**cURL 命令**:

```
Bash
运行

curl -X POST http://localhost:5000/
api/report/mood \
  -H "Content-Type: application/
  json" \
  -d '{
    "mood_data": {
      "current_mood": "happy",
      "mood_intensity": 7,
      "mood_triggers":
      ["work_success"]
    }
  }'

```

### 2.5 更新成长印记

**接口**: **POST /api/report/growth_journal**

**描述**: 更新成长印记 (Growth Journal) 记录

**请求参数**:

```
JSON

{
  "journal_entry": {
    "date": "2024-01-01",
    "reflection": "今天的成长反思",
    "achievements": ["完成了重要项目
    "],
    "challenges": ["时间管理需要改进"]
  }
}

```

**响应示例**:

```
JSON

{
  "status": "success",
  "message": "成长印记已更新",
  "entry_id": "journal_123"
}

```

**cURL 命令**:

```
Bash
运行

curl -X POST http://localhost:5000/
api/report/growth_journal \
  -H "Content-Type: application/
  json" \
  -d '{
    "journal_entry": {
      "date": "2024-01-01",
      "reflection": "今天的成长反思",
      "achievements": ["完成了重要项目
      "]
    }
  }'

```

### 2.6 生成综合心理画像报告

**接口**: **POST /api/report/holistic**

**描述**: 基于价值观和大五模型数据生成综合心理画像报告

**请求参数**:

```
JSON

{
  "core_values_data": {
    "core_values": ["成就", "自主"],
    "value_scores": {"achievement":
    8, "autonomy": 7}
  },
  "big_five_data": {
    "openness": 75,
    "conscientiousness": 68,
    "extraversion": 82,
    "agreeableness": 71,
    "neuroticism": 45
  }
}

```

**响应示例**:

```
JSON

{
  "status": "success",
  "report": {
    "personality_profile": "综合人格
    画像",
    "strengths": ["优势1", "优势2"],
    "development_areas": ["发展领域
    1"],
    "career_suggestions": ["职业建议
    1"],
    "relationship_insights": "人际关
    系洞察"
  }
}

```

**cURL 命令**:

```
Bash
运行

curl -X POST http://localhost:5000/
api/report/holistic \
  -H "Content-Type: application/
  json" \
  -d '{
    "core_values_data": {
      "core_values": ["成就", "自主
      "],
      "value_scores":
      {"achievement": 8,
      "autonomy": 7}
    },
    "big_five_data": {
      "openness": 75,
      "conscientiousness": 68,
      "extraversion": 82,
      "agreeableness": 71,
      "neuroticism": 45
    }
  }'

```

---

## 错误响应格式

所有 API 在出错时都会返回统一的错误格式：

```
JSON

{
  "error": "错误描述信息",
  "status": "error"
}

```

**常见错误码**:

- **400**: 请求参数错误
- **500**: 服务器内部错误

---

## 测试建议

1. **健康检查**: 首先测试 **/api/chat/health** 确保服务正常
    
2. **聊天功能**: 测试同步聊天接口验证基本功能
    
3. **报告生成**: 按需测试各种报告生成接口
    
4. **流式响应**: 使用支持 SSE 的客户端测试流式聊天接口
    
**注意事项**:

- 确保 OpenAI API 密钥已正确配置
- 某些报告接口可能需要特定的数据格式
- 流式接口需要支持 Server-Sent Events 的客户端