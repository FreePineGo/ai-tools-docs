# Codex / OpenAI 代码模型使用指南

## 什么是 Codex？

Codex 是 OpenAI 开发的 AI 代码生成模型，基于 GPT 架构专门针对代码理解和生成进行了优化。它能够将自然语言描述转换为可执行的代码，支持多种编程语言。

> **注意**: OpenAI 已于 2023 年停止 Codex 的独立 API 服务，其功能已整合到 GPT-4 和 GPT-4 Turbo 模型中。本文档同时涵盖 Codex 历史用法和当前 GPT-4 代码能力的最佳实践。

## 核心能力

- **代码生成**: 根据自然语言描述生成代码
- **代码补全**: 自动完成代码片段
- **代码翻译**: 在不同编程语言之间转换代码
- **代码解释**: 解释现有代码的功能
- **Bug 修复**: 识别并修复代码中的错误
- **测试生成**: 自动生成单元测试

## 支持的编程语言

Codex/GPT-4 支持超过 50 种编程语言，包括但不限于：

| 语言 | 支持程度 |
|------|----------|
| Python | ⭐⭐⭐⭐⭐ |
| JavaScript/TypeScript | ⭐⭐⭐⭐⭐ |
| Java | ⭐⭐⭐⭐⭐ |
| C/C++ | ⭐⭐⭐⭐⭐ |
| Go | ⭐⭐⭐⭐⭐ |
| Rust | ⭐⭐⭐⭐ |
| SQL | ⭐⭐⭐⭐⭐ |
| HTML/CSS | ⭐⭐⭐⭐⭐ |
| Shell/Bash | ⭐⭐⭐⭐ |
| PHP | ⭐⭐⭐⭐ |
| Ruby | ⭐⭐⭐⭐ |
| Swift | ⭐⭐⭐⭐ |

## 快速开始

### 1. 获取 API 密钥

1. 访问 [OpenAI 官网](https://openai.com/)
2. 注册/登录账户
3. 进入 [API Keys 页面](https://platform.openai.com/api-keys)
4. 创建新的 API 密钥

### 2. 安装依赖

```bash
# Python
pip install openai

# Node.js
npm install openai
```

### 3. 基本使用

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "写一个 Python 函数计算斐波那契数列"}
    ]
)

print(response.choices[0].message.content)
```

## 文档结构

- [API_GUIDE.md](./API_GUIDE.md) - 详细的 API 使用指南
- [EXAMPLES.md](./EXAMPLES.md) - 丰富的代码示例
- [PROMPTS.md](./PROMPTS.md) - Prompt 编写技巧
- [FAQ.md](./FAQ.md) - 常见问题解答

## 最佳实践概览

1. **明确具体**: 描述越详细，结果越准确
2. **分步请求**: 复杂任务拆分成多个步骤
3. **提供上下文**: 包含相关代码和背景信息
4. **验证输出**: 始终审查和测试生成的代码
5. **迭代优化**: 根据结果调整 prompt

## 注意事项

⚠️ **安全提醒**:
- 不要将 API 密钥硬编码在代码中
- 生成的代码可能存在安全漏洞，需仔细审查
- 不要用于生成恶意代码或绕过安全措施
- 注意代码的许可证和版权问题

⚠️ **局限性**:
- 可能生成看似正确但实际错误的代码
- 对最新库版本的支持可能滞后
- 复杂逻辑可能需要多次迭代
- 无法访问外部资源或执行代码

---

*最后更新：2026-03-15*
