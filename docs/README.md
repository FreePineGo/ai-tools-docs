# 📚 文档总索引

欢迎使用 AI Publisher Agent 文档中心！

## 🚀 快速入门

如果你是第一次使用，请按以下顺序阅读：

1. **[PRD.md](PRD.md)** - 产品需求文档，了解项目目标
2. **[USER_PERSONAS.md](USER_PERSONAS.md)** - 用户角色说明
3. **[CONTENT_STRUCTURE.md](CONTENT_STRUCTURE.md)** - 内容结构概览

## 📖 文档导航

### AI 编码助手文档

| 助手 | 说明 | 入口文档 |
|------|------|----------|
| **Aider** | CLI 驱动的 AI 编程助手 | [aider/README.md](aider/README.md) |
| **Claude Code** | Anthropic 官方 CLI 工具 | [claude-code/README.md](claude-code/README.md) |
| **Codex** | OpenAI Codex CLI | [codex/README.md](codex/README.md) |
| **Copilot** | GitHub Copilot | [copilot/README.md](copilot/README.md) |
| **Cursor** | AI 代码编辑器 | [cursor/README.md](cursor/README.md) |
| **Windsurf** | Codeium AI IDE | [windsurf/README.md](windsurf/README.md) |

### OpenClaw 框架文档

| 文档 | 说明 |
|------|------|
| [openclaw/README.md](openclaw/README.md) | OpenClaw 框架介绍 |
| [openclaw/INSTALL.md](openclaw/INSTALL.md) | 安装指南 |
| [openclaw/QUICKSTART.md](openclaw/QUICKSTART.md) | 快速开始 |
| [openclaw/COMMANDS.md](openclaw/COMMANDS.md) | 命令参考 |
| [openclaw/CONFIG.md](openclaw/CONFIG.md) | 配置说明 |
| [openclaw/AGENT_DEV.md](openclaw/AGENT_DEV.md) | Agent 开发指南 |
| [openclaw/FAQ.md](openclaw/FAQ.md) | 常见问题 |

### 使用指南

| 指南 | 说明 |
|------|------|
| [guides/SELECTION.md](guides/SELECTION.md) | 如何选择 AI 助手 |
| [guides/COMPARISON.md](guides/COMPARISON.md) | AI 助手对比 |
| [guides/WORKFLOWS.md](guides/WORKFLOWS.md) | 推荐工作流程 |
| [guides/TIPS.md](guides/TIPS.md) | 使用技巧 |

## 🔍 搜索建议

### 按主题搜索

- **安装配置**: 在各助手的 `INSTALL.md` 中查看
- **命令参考**: 查看各助手的 `COMMANDS.md` 或使用 `guides/` 下的对比文档
- **最佳实践**: 参考 `claude-code/BEST_PRACTICES.md` 或 `guides/TIPS.md`
- **问题排查**: 查看各助手的 `FAQ.md`

### 使用命令行搜索

```bash
# 在文档中搜索关键词
grep -r "关键词" docs/

# 或使用 PowerShell
Select-String -Path "docs\*" -Pattern "关键词" -Recurse
```

## 📁 文档结构

```text
docs/
├── README.md              # 本文档 - 总索引
├── INDEX.md               # 完整文档索引（详细版）
├── PRD.md                 # 产品需求文档
├── USER_PERSONAS.md       # 用户角色
├── CONTENT_STRUCTURE.md   # 内容结构
├── aider/                 # Aider 文档
├── claude-code/           # Claude Code 文档
├── codex/                 # Codex 文档
├── copilot/               # Copilot 文档
├── cursor/                # Cursor 文档
├── guides/                # 使用指南
├── openclaw/              # OpenClaw 框架文档
└── windsurf/              # Windsurf 文档
```

## 🤝 贡献指南

欢迎贡献文档！请遵循以下步骤：

### 1. 找到问题或改进点

- 文档缺失、错误或不清晰
- 需要补充示例或说明
- 发现过时的内容

### 2. 提交方式

- **小修改**: 直接编辑对应文档并提交
- **大修改**: 先在相关文档中创建 issue 或 TODO 注释
- **新文档**: 在对应目录下创建，并在本索引中添加链接

### 3. 文档规范

- 使用 Markdown 格式
- 标题层级清晰（H1 → H2 → H3）
- 代码块标注语言类型
- 链接使用相对路径
- 保持简洁明了

### 4. 更新索引

添加新文档后，请同步更新：
- `docs/README.md`（总索引）
- `docs/INDEX.md`（详细索引）

---

**最后更新**: 2026-03-15  
**维护者**: AI Publisher Agent 团队
