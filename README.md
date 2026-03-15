# 🤖 AI Publisher Agent

一个智能内容发布助手，基于 OpenClaw 框架构建。

---

## 📖 文档导航

**👉 从 [文档总索引](docs/README.md) 开始浏览完整文档**

### 快速链接

| 类别 | 文档 |
|------|------|
| **开始使用** | [产品需求](docs/PRD.md) · [用户角色](docs/USER_PERSONAS.md) · [内容结构](docs/CONTENT_STRUCTURE.md) |
| **AI 助手** | [Aider](docs/aider/README.md) · [Claude Code](docs/claude-code/README.md) · [Codex](docs/codex/README.md) · [Copilot](docs/copilot/README.md) · [Cursor](docs/cursor/README.md) · [Windsurf](docs/windsurf/README.md) |
| **OpenClaw** | [介绍](docs/openclaw/README.md) · [安装](docs/openclaw/INSTALL.md) · [快速开始](docs/openclaw/QUICKSTART.md) · [命令](docs/openclaw/COMMANDS.md) · [配置](docs/openclaw/CONFIG.md) · [Agent 开发](docs/openclaw/AGENT_DEV.md) · [FAQ](docs/openclaw/FAQ.md) |
| **使用指南** | [如何选择](docs/guides/SELECTION.md) · [工具对比](docs/guides/COMPARISON.md) · [工作流程](docs/guides/WORKFLOWS.md) · [使用技巧](docs/guides/TIPS.md) |

---

## 🚀 快速入门

### 1. 了解项目

首先阅读核心文档了解项目定位：

```bash
# 产品需求文档
docs/PRD.md

# 用户角色说明
docs/USER_PERSONAS.md

# 内容结构概览
docs/CONTENT_STRUCTURE.md
```

### 2. 选择你的 AI 助手

根据你的需求选择合适的 AI 编码助手：

- **Claude Code**: 强大推理能力，适合复杂任务
- **Aider**: CLI 驱动，Git 集成优秀
- **Codex**: OpenAI 生态，API 灵活
- **Cursor/Windsurf**: AI 原生 IDE 体验

📚 详细对比见：[docs/guides/SELECTION.md](docs/guides/SELECTION.md)

### 3. 安装 OpenClaw

```bash
# 安装 OpenClaw 框架
npm install -g openclaw

# 查看安装指南
# docs/openclaw/INSTALL.md
```

### 4. 开始使用

```bash
# 查看可用命令
openclaw help

# 快速开始
openclaw quickstart
```

---

## 📁 项目结构

```
ai-publisher-agent/
├── README.md                 # 本文件 - 项目介绍
├── docs/                     # 文档目录
│   ├── README.md            # 📚 文档总索引（从这里开始！）
│   ├── INDEX.md             # 📑 完整文档索引（详细版）
│   ├── PRD.md               # 产品需求文档
│   ├── USER_PERSONAS.md     # 用户角色
│   ├── CONTENT_STRUCTURE.md # 内容结构
│   ├── aider/               # Aider 文档
│   ├── claude-code/         # Claude Code 文档
│   ├── codex/               # Codex 文档
│   ├── copilot/             # Copilot 文档
│   ├── cursor/              # Cursor 文档
│   ├── guides/              # 使用指南
│   ├── openclaw/            # OpenClaw 框架文档
│   └── windsurf/            # Windsurf 文档
├── skills/                   # Agent Skills
├── memory/                   # 记忆文件
└── ...
```

---

## 🔍 搜索文档

### 在线浏览

直接访问 [docs/README.md](docs/README.md) 浏览完整文档索引。

### 命令行搜索

```bash
# PowerShell: 在文档中搜索关键词
Select-String -Path "docs\*" -Pattern "关键词" -Recurse

# Git Bash: 使用 grep
grep -r "关键词" docs/
```

### 按主题查找

| 需求 | 推荐文档 |
|------|----------|
| 安装配置 | `docs/openclaw/INSTALL.md`, `docs/claude-code/INSTALL.md` |
| 命令参考 | `docs/openclaw/COMMANDS.md`, `docs/claude-code/COMMANDS.md` |
| 最佳实践 | `docs/claude-code/BEST_PRACTICES.md`, `docs/guides/TIPS.md` |
| 问题排查 | `docs/openclaw/FAQ.md`, `docs/claude-code/FAQ.md` |
| 开发指南 | `docs/openclaw/AGENT_DEV.md` |

---

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

### 1. 发现改进点

- 📝 文档缺失、错误或不清晰
- 💡 需要补充示例或说明
- 🔄 发现过时的内容

### 2. 提交修改

**小修改**（错别字、链接修复等）:
- 直接编辑对应文档
- 提交更改

**大改动**（新增章节、重构内容等）:
- 在相关文档中添加 TODO 注释说明计划
- 或直接提交 PR

**新增文档**:
- 在对应分类目录下创建新文件
- 更新 `docs/README.md` 和 `docs/INDEX.md` 添加链接

### 3. 文档规范

- ✅ 使用 Markdown 格式
- ✅ 标题层级清晰（# → ## → ###）
- ✅ 代码块标注语言类型
- ✅ 链接使用相对路径
- ✅ 保持简洁明了
- ✅ 中英文混排时注意空格

### 4. 更新索引

添加或修改文档后，请同步更新：

```bash
# 更新总索引
docs/README.md

# 更新详细索引
docs/INDEX.md
```

---

## 📞 支持

遇到问题？查看以下资源：

1. **[FAQ 合集](docs/openclaw/FAQ.md)** - 常见问题解答
2. **[使用技巧](docs/guides/TIPS.md)** - 实用技巧和问题规避
3. **[问题排查](docs/claude-code/FAQ.md)** - 特定工具问题

---

## 📄 许可证

本项目采用开源许可证。详见 LICENSE 文件。

---

**最后更新**: 2026-03-15  
**维护者**: AI Publisher Agent 团队  
**版本**: 1.0

---

🌟 **开始探索**: [docs/README.md](docs/README.md) - 文档总索引
