# API 使用指南

## 概述

本文档详细介绍如何使用 OpenAI API 进行代码生成和相关任务。虽然 Codex API 已停用，但 GPT-4 系列模型提供了相同的代码能力。

## 认证与设置

### 环境变量配置

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Windows CMD
set OPENAI_API_KEY=your-api-key-here
```

### 配置文件方式

创建 `.env` 文件：
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_ORG_ID=org-xxxxxxxxxxxxxxxxxxxxxxxx  # 可选
```

## Python SDK 使用

### 安装

```bash
pip install openai python-dotenv
```

### 基础示例

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# 代码生成
def generate_code(prompt: str, language: str = "python") -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"你是一个专业的{language}程序员。只输出代码，不要解释。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2000
    )
    return response.choices[0].message.content

# 使用示例
code = generate_code("创建一个快速排序函数")
print(code)
```

### 高级配置

```python
def advanced_code_generation(
    prompt: str,
    model: str = "gpt-4",
    temperature: float = 0.2,
    max_tokens: int = 4000,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: list = None
) -> str:
    """
    高级代码生成函数
    
    Args:
        prompt: 用户请求
        model: 模型名称
        temperature: 创造性程度 (0-2)，代码生成建议 0.1-0.3
        max_tokens: 最大输出长度
        top_p: 核采样参数
        frequency_penalty: 频率惩罚
        presence_penalty: 存在惩罚
        stop: 停止序列
    
    Returns:
        生成的代码
    """
    client = OpenAI()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是专家程序员"},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    
    return response.choices[0].message.content
```

## Node.js SDK 使用

### 安装

```bash
npm install openai dotenv
```

### 基础示例

```javascript
import OpenAI from 'openai';
import dotenv from 'dotenv';

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function generateCode(prompt, language = 'javascript') {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: `你是一个专业的${language}程序员。只输出代码。`
      },
      {
        role: 'user',
        content: prompt
      }
    ],
    temperature: 0.2,
    max_tokens: 2000,
  });

  return completion.choices[0].message.content;
}

// 使用
const code = await generateCode('创建一个 HTTP 服务器');
console.log(code);
```

## REST API 直接调用

### HTTP 请求示例

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {
        "role": "system",
        "content": "你是 Python 专家"
      },
      {
        "role": "user",
        "content": "写一个装饰器来缓存函数结果"
      }
    ],
    "temperature": 0.2,
    "max_tokens": 2000
  }'
```

### Python requests 示例

```python
import requests
import os

def call_api(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "你是编程助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    return result['choices'][0]['message']['content']
```

## 流式响应

### Python 流式示例

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "写一个 Python 脚本"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

### Node.js 流式示例

```javascript
const stream = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: '写代码' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

## 错误处理

```python
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "写代码"}]
    )
except AuthenticationError:
    print("API 密钥无效或已过期")
except RateLimitError:
    print("请求过于频繁，请稍后重试")
except APIError as e:
    print(f"API 错误：{e}")
except Exception as e:
    print(f"未知错误：{e}")
```

## 使用技巧

### 1. 系统消息优化

```python
messages = [
    {
        "role": "system",
        "content": """你是资深软件工程师。
        - 只输出代码，不解释
        - 使用最佳实践
        - 添加必要的注释
        - 包含错误处理"""
    },
    {"role": "user", "content": "你的请求"}
]
```

### 2. 上下文管理

```python
# 多轮对话保持上下文
conversation = [
    {"role": "system", "content": "你是 Python 助手"},
    {"role": "user", "content": "创建一个类"},
    {"role": "assistant", "content": "class MyClass:..."},
    {"role": "user", "content": "添加一个方法"}  # 模型知道是哪个类
]
```

### 3. 代码提取

```python
import re

def extract_code(response: str, language: str = "python") -> str:
    """从响应中提取代码块"""
    pattern = f"```{language}\\n(.*?)```"
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1) if match else response
```

## 成本优化

### 1. 选择合适的模型

| 模型 | 代码能力 | 成本 | 推荐场景 |
|------|----------|------|----------|
| GPT-4 | ⭐⭐⭐⭐⭐ | 高 | 复杂任务、生产代码 |
| GPT-4 Turbo | ⭐⭐⭐⭐⭐ | 中 | 日常开发 |
| GPT-3.5 Turbo | ⭐⭐⭐⭐ | 低 | 简单任务、原型 |

### 2. Token 优化

```python
# 精简 prompt
# ❌ 冗长
prompt = "请帮我写一个 Python 函数，这个函数要能够接收一个列表作为参数，然后返回列表中的最大值..."

# ✅ 简洁
prompt = "Python 函数：返回列表最大值"
```

### 3. 缓存结果

```python
import hashlib
import json

cache = {}

def cached_generation(prompt: str) -> str:
    key = hashlib.md5(prompt.encode()).hexdigest()
    if key in cache:
        return cache[key]
    
    result = generate_code(prompt)
    cache[key] = result
    return result
```

## 安全最佳实践

1. **密钥管理**: 使用环境变量或密钥管理服务
2. **输入验证**: 验证和清理用户输入
3. **输出审查**: 始终审查生成的代码
4. **速率限制**: 实现客户端限流
5. **日志记录**: 记录 API 调用用于审计

---

*最后更新：2026-03-15*
