# Cursor - AI 代码编辑器使用指南

## 工具简介

Cursor 是一款基于 VS Code 构建的 AI 原生代码编辑器，将 AI 深度集成到开发工作流中。它支持多种大语言模型（包括 GPT-4、Claude 等），能够理解整个代码库的上下文，提供智能的代码生成、编辑和调试功能。

**核心优势：**
- 基于 VS Code，兼容所有 VS Code 扩展
- 深度代码库理解，支持跨文件上下文
- 自然的对话式编程体验
- 支持多种 AI 模型切换

## 安装步骤

### Windows/macOS/Linux

1. **访问官网下载**
   - 打开 https://cursor.sh
   - 点击 "Download" 按钮
   - 选择对应操作系统的版本

2. **安装应用**
   - Windows：运行下载的 `.exe` 安装程序
   - macOS：将 Cursor 拖拽到 Applications 文件夹
   - Linux：下载 `.AppImage` 或使用包管理器

3. **首次启动配置**
   - 启动 Cursor
   - 使用 GitHub 或邮箱账号登录
   - 导入 VS Code 设置和扩展（可选）

4. **API Key 配置（可选）**
   - 打开设置（`Ctrl+,` 或 `Cmd+,`）
   - 进入 "AI" 或 "General" 设置
   - 添加自己的 API Key 以获得更高配额

## 基本用法

### 1. AI 聊天（Chat）

```
快捷键：Ctrl+L (Windows/Linux) / Cmd+L (Mac)
```

- 在侧边栏打开聊天面板
- 输入自然语言描述需求
- AI 会生成代码或解答问题
- 支持引用特定文件：`@filename`

### 2. 行内编辑（Inline Edit）

```
快捷键：Ctrl+K (Windows/Linux) / Cmd+K (Mac)
```

- 选中需要修改的代码
- 按下快捷键，输入修改指令
- AI 直接在原位置生成修改后的代码
- 支持 diff 预览和接受/拒绝

### 3. 代码生成（Generate）

```
快捷键：Ctrl+I (Windows/Linux) / Cmd+I (Mac)
```

- 在空白处或注释后使用
- 描述需要生成的代码功能
- AI 自动补全完整实现

### 4. 命令面板（Command）

```
快捷键：Ctrl+Shift+P (Windows/Linux) / Cmd+Shift+P (Mac)
```

- 输入 "Cursor" 相关命令
- 快速访问 AI 功能
- 如："Cursor: Focus on Chat"

## 特色功能

### 🧠 代码库理解（Codebase Understanding）

- **自动索引**：Cursor 自动索引整个项目
- **智能检索**：AI 能理解跨文件的代码关系
- **上下文感知**：回答问题时自动引用相关文件

### 🔍 智能搜索（Semantic Search）

- 使用自然语言搜索代码
- 例如："查找处理用户登录的函数"
- 比传统文本搜索更准确

### 🤖 多模型支持

- **Cursor Fast**：快速响应，适合简单任务
- **GPT-4**：强大的通用能力
- **Claude 3.5 Sonnet**：优秀的代码理解
- **自定义模型**：支持配置自己的 API

### 📝 Tab 自动补全

- 智能代码补全，超越传统 Intellisense
- 根据上下文预测整行或整块代码
- 按 `Tab` 接受建议

### 🐛 智能调试

- 自动分析错误信息
- 提供修复建议
- 支持一键应用修复

## 使用技巧

### 💡 高效提示词技巧

1. **具体明确**
   ```
   ❌ "修复这个 bug"
   ✅ "修复第 45 行的空指针异常，当 userInput 为 null 时"
   ```

2. **提供上下文**
   ```
   @utils/auth.ts 帮我添加 JWT 验证逻辑
   ```

3. **分步请求**
   ```
   第一步：创建用户模型
   第二步：添加验证规则
   第三步：编写测试用例
   ```

### 🎯 最佳实践

1. **使用 @ 引用文件**
   - 在聊天中输入 `@` 可快速引用文件
   - 帮助 AI 理解具体上下文

2. **利用 Composer 功能**
   - 多文件编辑时，使用 Composer 模式
   - AI 会协调多个文件的修改

3. **Review AI 代码**
   - 始终审查 AI 生成的代码
   - 理解每处修改的意图
   - 确保符合项目规范

4. **合理使用配额**
   - 简单任务用 Fast 模型
   - 复杂任务用 GPT-4/Claude
   - 关注配额使用情况

### ⚡ 快捷操作

| 操作 | 快捷键 | 说明 |
|------|--------|------|
| 打开聊天 | Ctrl/Cmd + L | 打开 AI 聊天面板 |
| 行内编辑 | Ctrl/Cmd + K | 选中代码后编辑 |
| 代码生成 | Ctrl/Cmd + I | 在光标处生成代码 |
| 接受建议 | Tab | 接受自动补全 |
| 拒绝建议 | Esc | 拒绝自动补全 |
| 切换模型 | Ctrl/Cmd + Shift + M | 切换 AI 模型 |

### 🔧 配置建议

```json
// settings.json 推荐配置
{
  "cursor.ai.enabled": true,
  "cursor.tabAutocomplete": true,
  "cursor.quickActions.enabled": true,
  "cursor.indexing.enabled": true,
  "cursor.indexing.ignore": ["node_modules", "dist", ".git"]
}
```

### 🚀 进阶用法

1. **批量重构**
   - 描述重构目标，让 AI 列出所有需要修改的文件
   - 使用 Composer 一次性应用修改

2. **代码审查**
   - 选中代码，让 AI 提供改进建议
   - 询问潜在的性能问题或安全隐患

3. **文档生成**
   - 让 AI 根据代码生成注释和文档
   - 自动生成 README 或 API 文档

4. **测试编写**
   - 提供函数代码，让 AI 生成测试用例
   - 覆盖边界情况和错误场景

---

**官方资源：**
- 官网：https://cursor.sh
- 文档：https://docs.cursor.com
- 社区：https://forum.cursor.com
