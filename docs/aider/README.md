# Aider - CLI AI 编程工具使用指南

## 工具简介

Aider 是一款命令行界面的 AI 编程助手，专为开发者设计。它可以直接在终端中与 AI 对话，自动编辑项目文件，支持 Git 版本控制，并能够理解整个代码库的上下文。Aider 适合喜欢终端工作流的开发者，支持多种大语言模型。

**核心优势：**
- 纯命令行操作，无需离开终端
- 自动 Git 集成，每次修改自动提交
- 支持多种 AI 模型（GPT-4、Claude、本地模型等）
- 项目级代码理解
- 开源免费使用

## 安装步骤

### 前置要求

- Python 3.9 或更高版本
- pip 包管理器
- Git（用于版本控制功能）

### 1. 安装 Aider

```bash
# 使用 pip 安装（推荐）
pip install aider-chat

# 或使用 pipx（隔离环境）
pipx install aider-chat

# 验证安装
aider --version
```

### 2. 配置 API Key

Aider 支持多种 AI 模型，需要配置相应的 API Key：

#### 使用 OpenAI

```bash
# 设置环境变量
export OPENAI_API_KEY=your-api-key-here

# 或在 Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# 或在 .env 文件中配置
echo "OPENAI_API_KEY=your-api-key-here" >> .env
```

#### 使用 Anthropic (Claude)

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

#### 使用其他模型

```bash
# Google Gemini
export GEMINI_API_KEY=your-api-key-here

# Groq
export GROQ_API_KEY=your-api-key-here

# 本地模型 (Ollama)
# 无需 API Key，确保 Ollama 服务运行中
```

### 3. 配置 Git（推荐）

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 配置 Git 用户信息
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 创建初始提交
git add .
git commit -m "Initial commit"
```

### 4. 首次运行

```bash
# 进入项目目录
cd your-project

# 启动 Aider
aider

# 或指定模型
aider --model gpt-4o

# 或指定多个文件
aider src/main.py src/utils.py
```

## 基本用法

### 1. 启动 Aider

```bash
# 基本启动
aider

# 指定模型
aider --model claude-3-5-sonnet

# 指定文件
aider src/app.py

# 只读模式（不修改文件）
aider --read-only

# 禁用 Git 自动提交
aider --no-auto-commits
```

### 2. 与 AI 对话

启动 Aider 后，进入交互式对话模式：

```
> 帮我创建一个用户登录函数

> 给这个函数添加错误处理

> 重构这个模块，使用类来组织代码

> 为这些函数编写单元测试
```

### 3. 常用命令

```
/exit          - 退出 Aider
/undo          - 撤销最后一次修改
/diff          - 显示当前变更
/commit        - 手动提交变更
/model         - 查看或切换模型
/tokens        - 显示 token 使用情况
/clear         - 清空聊天历史
/help          - 显示帮助信息
/run           - 运行 shell 命令
/add           - 添加文件到上下文
/drop          - 从上下文移除文件
```

### 4. 添加文件到上下文

```bash
# 在对话中
/add src/utils.py
/add docs/*.md

# 启动时指定
aider src/main.py src/config.py
```

## 特色功能

### 🤖 多模型支持

**支持的模型：**
- OpenAI: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- Anthropic: claude-3-5-sonnet, claude-3-opus, claude-3-haiku
- Google: gemini-pro, gemini-1.5-pro
- Groq: llama-3-70b, mixtral-8x7b
- 本地模型：Ollama, LM Studio

**切换模型：**
```bash
# 启动时指定
aider --model claude-3-5-sonnet

# 对话中切换
/model claude-3-5-sonnet
```

### 📁 项目级理解

- **自动索引**：Aider 自动分析项目结构
- **智能检索**：根据上下文引用相关文件
- **跨文件编辑**：理解文件间依赖关系
- **代码导航**：快速定位相关代码

### 🔀 Git 集成

**自动版本控制：**
- 每次 AI 修改后自动创建 Git 提交
- 提交信息描述变更内容
- 支持撤销（/undo）
- 保持完整的变更历史

**手动控制：**
```bash
# 禁用自动提交
aider --no-auto-commits

# 手动提交
/commit

# 查看变更
/diff

# 撤销修改
/undo
```

### 🎯 智能文件管理

```bash
# 添加文件到上下文
/add filename.py

# 添加多个文件
/add file1.py file2.py

# 使用通配符
/add src/*.py

# 移除文件
/drop filename.py

# 查看当前上下文
/ls
```

### 🛠️ 终端命令执行

```bash
# 在 Aider 中运行命令
/run npm install

/run python test.py

/run git status
```

### 📊 Token 管理

```bash
# 查看 token 使用情况
/tokens

# 查看模型成本
/model --cost
```

## 使用技巧

### 💡 高效提示词技巧

1. **具体明确**
   ```
   ❌ "修复 bug"
   ✅ "修复第 45 行的空指针异常，当 user_input 为 None 时"
   ```

2. **提供上下文**
   ```
   /add src/auth.py
   帮我在这个文件中添加 JWT 验证
   ```

3. **分步执行**
   ```
   第一步：创建数据库模型
   第二步：添加验证逻辑
   第三步：编写 API 端点
   第四步：生成测试用例
   ```

### 🎯 最佳实践

1. **初始化 Git 仓库**
   ```bash
   # 在使用 Aider 前
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **合理选择模型**
   ```bash
   # 简单任务 - 使用快速/便宜模型
   aider --model gpt-3.5-turbo
   
   # 复杂任务 - 使用强大模型
   aider --model claude-3-5-sonnet
   ```

3. **管理上下文文件**
   ```bash
   # 只添加相关文件，避免 token 浪费
   /add src/user_service.py
   /add src/models/user.py
   
   # 完成后清理
   /drop src/user_service.py
   ```

4. **审查 AI 修改**
   ```bash
   # 查看变更
   /diff
   
   # 不满意就撤销
   /undo
   
   # 满意后提交
   /commit
   ```

### ⚡ 常用工作流

#### 1. 新功能开发

```bash
# 启动 Aider，添加相关文件
aider src/api/ src/models/

# 描述需求
> 创建一个新的用户注册 API 端点
> 需要包含邮箱验证和密码强度检查

# 审查修改
/diff

# 运行测试
/run pytest tests/test_registration.py

# 提交
/commit
```

#### 2. 代码重构

```bash
# 添加要重构的文件
/add src/legacy_module.py

# 描述重构目标
> 将这个模块重构为使用现代 Python 特性
> 使用类型注解和 dataclass

# 审查并测试
/diff
/run python -m pytest

# 提交
/commit
```

#### 3. Bug 修复

```bash
# 添加相关文件
/add src/error_handler.py

# 提供错误信息
> 修复这个错误：[粘贴错误信息]
> 错误发生在用户登录时

# 验证修复
/run python test_login.py

# 提交
/commit
```

#### 4. 测试编写

```bash
# 添加源代码文件
/add src/calculator.py

# 请求生成测试
> 为这个模块编写完整的单元测试
> 覆盖所有边界情况

# 运行测试
/run pytest tests/test_calculator.py -v

# 提交
/commit
```

### 🔧 配置选项

```bash
# .aider.conf.yml 配置文件

model: claude-3-5-sonnet
auto-commits: true
dirty-commits: true
attribute-author: true
attribute-committer: true
map-tokens: 1024
max-chat-history-tokens: 4096
```

### 📋 命令行参数

```bash
# 常用参数

--model MODEL          # 指定 AI 模型
--no-auto-commits      # 禁用自动提交
--read-only            # 只读模式
--dark-mode            # 深色主题
--light-mode           # 浅色主题
--verbose              # 详细输出
--analytics            # 启用分析

--file FILE            # 添加文件
--message MSG          # 初始消息
--commit               # 提交变更
--help                 # 显示帮助
```

### 🚀 进阶用法

1. **批量处理**
   ```bash
   # 为多个文件生成文档
   aider --message "为这些文件生成 docstring" src/*.py
   ```

2. **代码审查**
   ```bash
   # 让 AI 审查代码
   /add src/main.py
   > 审查这段代码，找出潜在问题和改进建议
   ```

3. **性能优化**
   ```bash
   /add src/slow_function.py
   > 分析这个函数的性能瓶颈并优化
   ```

4. **安全审计**
   ```bash
   /add src/auth.py
   > 检查这段代码的安全漏洞
   ```

5. **依赖更新**
   ```bash
   > 更新 requirements.txt 中的所有依赖到最新版本
   > 修复可能的兼容性问题
   ```

### 🛡️ 安全提示

1. **审查所有修改**
   - 使用 `/diff` 查看 AI 的所有修改
   - 特别是安全相关的代码
   - 确认没有引入漏洞

2. **敏感信息**
   - 不要在对话中分享 API Key
   - 使用环境变量管理敏感配置
   - 检查 AI 是否硬编码了密钥

3. **Git 历史**
   - 保持清晰的提交历史
   - 重要的修改手动编写提交信息
   - 定期审查 Git 日志

4. **依赖安全**
   - 审查 AI 建议的依赖更新
   - 检查新版本的安全性
   - 使用依赖扫描工具

---

**官方资源：**
- GitHub：https://github.com/paul-gauthier/aider
- 官网：https://aider.chat
- 文档：https://aider.chat/docs
- PyPI：https://pypi.org/project/aider-chat/
