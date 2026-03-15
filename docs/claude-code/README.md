# Claude Code 使用文档

## 简介

Claude Code 是 Anthropic 推出的命令行 AI 编程助手，它能够将自然语言指令转化为代码操作，帮助开发者更高效地完成编程任务。

### 核心特性

- **自然语言编程**: 用日常语言描述需求，Claude Code 自动执行代码操作
- **文件读写能力**: 可以读取、创建、修改项目文件
- **命令执行**: 安全地运行 shell 命令
- **上下文理解**: 理解项目结构和代码上下文
- **多轮对话**: 支持迭代式开发和调试

### 适用场景

- 🚀 快速搭建项目脚手架
- 🔧 代码重构和优化
- 📝 生成样板代码
- 🐛 调试和修复问题
- 📚 学习新技术和框架
- 🔍 代码审查和分析

### 文档结构

| 文档 | 说明 |
|------|------|
| [INSTALL.md](./INSTALL.md) | 详细安装指南 |
| [QUICKSTART.md](./QUICKSTART.md) | 快速入门教程 |
| [COMMANDS.md](./COMMANDS.md) | 命令参考手册 |
| [SKILLS.md](./SKILLS.md) | Skills 使用指南 |
| [BEST_PRACTICES.md](./BEST_PRACTICES.md) | 最佳实践 |
| [FAQ.md](./FAQ.md) | 常见问题解答 |

### 系统要求

- **操作系统**: macOS 10.15+, Linux, Windows 10+
- **Node.js**: v18.0 或更高版本
- **npm**: v9.0 或更高版本
- **网络**: 需要访问 Anthropic API

### 快速开始

```bash
# 安装
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version

# 开始使用
claude
```

---

**注意**: 使用 Claude Code 需要有效的 Anthropic API 密钥。请参考 [INSTALL.md](./INSTALL.md) 获取详细的配置说明。
