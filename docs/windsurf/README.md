# Windsurf - AI 开发环境使用指南

## 工具简介

Windsurf 是由 Codeium 开发的下一代 AI 原生 IDE，将 AI 深度集成到开发工作流的每一个环节。它基于 VS Code 构建，提供了超越传统代码补全的智能开发体验，包括项目级理解、智能工作流和深度上下文感知。

**核心优势：**
- 完全兼容 VS Code 生态系统
- 项目级 AI 理解（Cascade 引擎）
- 智能工作流自动化
- 免费且功能强大

## 安装步骤

### 1. 下载 Windsurf

1. **访问官网**
   - 打开 https://codeium.com/windsurf
   - 点击 "Download for Free"

2. **选择操作系统版本**
   - Windows：下载 `.exe` 安装程序
   - macOS：下载 `.dmg` 文件
   - Linux：下载 `.deb`、`.rpm` 或 `.AppImage`

### 2. 安装应用

#### Windows
```
1. 运行下载的 windsurf-setup.exe
2. 按照安装向导完成安装
3. 选择是否创建桌面快捷方式
4. 完成安装
```

#### macOS
```
1. 打开下载的 .dmg 文件
2. 将 Windsurf 拖拽到 Applications 文件夹
3. 在 Applications 中启动 Windsurf
```

#### Linux
```bash
# Debian/Ubuntu
sudo dpkg -i windsurf_amd64.deb

# Red Hat/Fedora
sudo rpm -i windsurf.x86_64.rpm

# 或使用 AppImage
chmod +x windsurf.AppImage
./windsurf.AppImage
```

### 3. 首次启动配置

```
1. 启动 Windsurf
2. 使用 GitHub、Google 或邮箱账号登录
3. 导入 VS Code 设置和扩展（可选）
4. 完成 Cascade AI 配置
5. 开始使用
```

### 4. 导入 VS Code 配置（可选）

```
1. 首次启动时会提示导入 VS Code 配置
2. 选择要导入的内容：
   - 设置（Settings）
   - 扩展（Extensions）
   - 快捷键（Keybindings）
   - 代码片段（Snippets）
3. 确认导入
```

## 基本用法

### 1. Cascade AI 聊天

```
快捷键：Ctrl+L (Windows/Linux) / Cmd+L (Mac)

功能：
- 打开侧边栏 AI 聊天面板
- 与 AI 对话获取代码帮助
- 支持项目级上下文理解
- 可执行文件操作和命令
```

### 2. 行内 AI 编辑

```
快捷键：Ctrl+I (Windows/Linux) / Cmd+I (Mac)

功能：
- 在编辑器内直接编辑代码
- 输入自然语言指令
- AI 直接修改选中的代码
- 支持 diff 预览
```

### 3. 智能补全

```
使用方式：
1. 开始编写代码
2. Windsurf 自动显示 AI 建议
3. Tab 接受建议
4. 支持多行补全
```

### 4. 命令面板

```
快捷键：Ctrl+Shift+P (Windows/Linux) / Cmd+Shift+P (Mac)

常用命令：
- Cascade: Chat
- Cascade: Edit
- Cascade: Run Command
- Cascade: Explain Code
```

## 特色功能

### 🌊 Cascade 引擎

**项目级 AI 理解：**
- 自动索引整个项目结构
- 理解文件间的依赖关系
- 基于项目上下文提供建议
- 支持跨文件代码生成

**智能工作流：**
- AI 可以执行文件操作
- 自动运行终端命令
- 创建/修改/删除文件
- 实时预览变更

### 🔍 深度上下文感知

- **文件上下文**：理解当前文件的所有内容
- **项目上下文**：理解整个项目的结构
- **Git 上下文**：了解代码变更历史
- **终端上下文**：关联终端输出

### 🤖 自主 Agent 能力

**Cascade 可以：**
- 搜索和阅读项目文件
- 运行终端命令
- 创建和修改文件
- 执行多步骤任务
- 调试和修复问题

### 📊 智能搜索

```
功能：
- 自然语言搜索代码
- 语义理解而非关键词匹配
- 快速定位相关代码
- 支持跨文件搜索
```

### 🎯 多模式交互

1. **Chat 模式**
   - 侧边栏对话
   - 适合复杂问题
   - 支持文件引用

2. **Edit 模式**
   - 行内编辑
   - 快速修改
   - 直接应用

3. **Agent 模式**
   - 自主执行任务
   - 多步骤操作
   - 实时反馈

### 🛠️ 开发工具集成

- **内置终端**：AI 可直接执行命令
- **Git 集成**：理解代码变更
- **调试器**：AI 辅助调试
- **扩展市场**：兼容 VS Code 扩展

## 使用技巧

### 💡 高效提示词技巧

1. **明确任务目标**
   ```
   ❌ "帮我改一下这个"
   ✅ "重构这个函数，使用 async/await 替代 Promise 链"
   ```

2. **提供充分上下文**
   ```
   在 Cascade 中：
   "查看 @src/api/user.ts 文件，添加输入验证逻辑"
   ```

3. **分步骤描述**
   ```
   "第一步：创建数据库连接
   第二步：编写查询函数
   第三步：添加错误处理"
   ```

### 🎯 最佳实践

1. **善用文件引用**
   - 使用 `@` 引用相关文件
   - 帮助 AI 理解完整上下文
   - 减少误解和错误

2. **利用 Agent 能力**
   - 让 Cascade 执行多步骤任务
   - 如："创建一个新的 React 组件，包含样式和测试"
   - AI 会自动创建所有必要文件

3. **审查 AI 操作**
   - 查看 AI 计划执行的操作
   - 确认后再应用
   - 特别是文件删除和命令执行

4. **保持项目整洁**
   - 清晰的目录结构帮助 AI 理解
   - 一致的命名规范
   - 完整的类型定义

### ⚡ 快捷键速查

| 操作 | Windows/Linux | Mac | 说明 |
|------|---------------|-----|------|
| 打开 Chat | Ctrl+L | Cmd+L | 打开 Cascade 聊天 |
| 行内编辑 | Ctrl+I | Cmd+I | 选中代码后编辑 |
| 接受补全 | Tab | Tab | 接受 AI 建议 |
| 拒绝补全 | Esc | Esc | 拒绝 AI 建议 |
| 命令面板 | Ctrl+Shift+P | Cmd+Shift+P | 打开命令面板 |
| 快速打开 | Ctrl+P | Cmd+P | 快速打开文件 |

### 🔧 配置建议

```json
// settings.json 推荐配置
{
  "codeium.enable": true,
  "codeium.enableChat": true,
  "codeium.enableCopilot": true,
  "codeium.indexing.enabled": true,
  "codeium.indexing.ignore": [
    "node_modules",
    "dist",
    "build",
    ".git",
    "*.min.js"
  ],
  "codeium.chat.maxContextFiles": 10,
  "codeium.autocomplete.enable": true
}
```

### 🚀 进阶用法

1. **项目脚手架生成**
   ```
   在 Cascade 中输入：
   "创建一个 Next.js 项目，包含以下功能：
   - 用户认证
   - 数据库连接
   - API 路由
   - 基础样式"
   
   AI 会自动创建完整的项目结构
   ```

2. **代码迁移**
   ```
   "将 src/classic/ 目录下的所有类组件
   转换为 React 函数组件"
   
   AI 会逐个文件处理并更新
   ```

3. **批量重构**
   ```
   "将项目中所有的 var 声明
   改为 const 或 let"
   
   AI 会分析并安全地替换
   ```

4. **调试辅助**
   ```
   选中报错的代码，在 Chat 中输入：
   "分析这个错误，找出原因并修复"
   
   AI 会分析错误并提供修复方案
   ```

5. **文档生成**
   ```
   "为整个 src/api/ 目录生成 API 文档"
   
   AI 会读取所有文件并生成完整文档
   ```

6. **测试套件生成**
   ```
   "为 src/utils/ 下的所有函数
   编写单元测试，使用 Jest"
   
   AI 会创建完整的测试文件
   ```

### 💻 终端集成

```
Cascade 可以直接执行终端命令：

1. 在 Chat 中输入：
   "运行 npm install"
   
2. AI 会在终端执行命令
   
3. 查看输出并继续对话：
   "安装失败了，查看错误信息"
```

### 🔐 安全提示

1. **审查文件操作**
   - AI 请求删除文件时仔细检查
   - 确认文件路径正确
   - 备份重要文件

2. **命令执行安全**
   - 审查 AI 要执行的命令
   - 特别是 rm、chmod 等危险命令
   - 避免执行未知来源的脚本

3. **敏感信息保护**
   - 不要在 Chat 中分享 API Key
   - 使用环境变量管理敏感配置
   - 检查 AI 生成的代码是否有硬编码密钥

---

**官方资源：**
- 官网：https://codeium.com/windsurf
- 文档：https://docs.codeium.com/windsurf
- 下载：https://codeium.com/windsurf/download
- 社区：https://discord.gg/codeium
