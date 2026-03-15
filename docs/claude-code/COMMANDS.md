# Claude Code 命令参考

## 命令行参数

### 基本命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `claude` | 启动交互式会话 | `claude` |
| `claude --version` | 显示版本信息 | `claude --version` |
| `claude --help` | 显示帮助信息 | `claude --help` |
| `claude [prompt]` | 执行单条指令 | `claude "解释这个文件"` |

### 配置选项

| 参数 | 简写 | 说明 |
|------|------|------|
| `--model <name>` | `-m` | 指定使用的模型 |
| `--max-tokens <n>` | `-t` | 设置最大 token 数 |
| `--timeout <ms>` | `-T` | 设置超时时间（毫秒） |
| `--config <path>` | `-c` | 指定配置文件路径 |
| `--verbose` | `-v` | 详细输出模式 |
| `--quiet` | `-q` | 静默模式 |
| `--json` | `-j` | JSON 格式输出 |

### 会话管理

| 参数 | 说明 |
|------|------|
| `--session <id>` | 加载指定会话 |
| `--new-session` | 创建新会话 |
| `--export <file>` | 导出会话到文件 |
| `--import <file>` | 从文件导入会话 |
| `--list-sessions` | 列出所有会话 |

## 内置命令（Slash Commands）

在交互式会话中可用的斜杠命令：

### 导航命令

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助信息 |
| `/clear` | 清除当前会话历史 |
| `/exit` | 退出会话 |
| `/quit` | 退出会话（同 /exit） |

### 文件命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/read` | 读取文件内容 | `/read src/app.ts` |
| `/write` | 写入文件 | `/write output.txt 内容` |
| `/edit` | 编辑文件 | `/edit config.json` |
| `/create` | 创建新文件 | `/create src/new.ts` |
| `/delete` | 删除文件 | `/delete temp.txt` |
| `/list` | 列出目录内容 | `/list src/` |

### 代码命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/search` | 搜索代码 | `/search "function test"` |
| `/run` | 运行命令 | `/run npm test` |
| `/build` | 构建项目 | `/build` |
| `/test` | 运行测试 | `/test` |
| `/lint` | 代码检查 | `/lint` |
| `/format` | 格式化代码 | `/format src/` |

### Git 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/git status` | 查看状态 | `/git status` |
| `/git add` | 添加文件 | `/git add .` |
| `/git commit` | 提交更改 | `/git commit -m "msg"` |
| `/git push` | 推送代码 | `/git push` |
| `/git pull` | 拉取代码 | `/git pull` |
| `/git log` | 查看历史 | `/git log` |
| `/git diff` | 查看差异 | `/git diff` |

### 配置命令

| 命令 | 说明 |
|------|------|
| `/config` | 查看当前配置 |
| `/config set` | 设置配置项 |
| `/config reset` | 重置配置 |
| `/model` | 切换模型 |
| `/prefs` | 查看偏好设置 |

## 自然语言指令模式

### 文件操作指令

```
# 读取文件
读取 @package.json
显示 @src/index.ts 的内容
查看配置文件

# 创建文件
创建一个新文件 src/utils/helper.ts
在 docs 文件夹创建 README.md
生成一个 TypeScript 配置文件

# 修改文件
修改 @app.ts，添加错误处理
更新 @config.json 中的端口设置
在 @styles.css 中添加新样式

# 删除文件
删除临时文件 temp.txt
移除 @old-module.js
清理构建输出目录
```

### 代码生成指令

```
# 生成代码
创建一个用户认证函数
生成一个 React 组件用于显示列表
编写一个 API 端点处理用户注册

# 重构代码
优化这个函数的性能
将这段代码转换为 TypeScript
提取重复逻辑为独立函数

# 添加功能
为这个类添加日志功能
实现缓存机制
添加输入验证
```

### 调试指令

```
# 分析问题
为什么这个测试失败了？
找出内存泄漏的原因
解释这个错误信息

# 修复问题
修复这个空指针异常
解决类型不匹配问题
修正 API 响应格式

# 优化代码
提高这个查询的性能
减少这个函数的复杂度
优化资源加载
```

### 项目指令

```
# 项目设置
初始化一个新的 Node.js 项目
设置 TypeScript 配置
配置 ESLint 和 Prettier

# 依赖管理
安装 express 和相关类型定义
更新所有依赖到最新版本
移除未使用的依赖

# 构建部署
构建生产版本
部署到 Vercel
生成 Docker 配置
```

## 文件引用语法

### 单文件引用

```
@filename           # 当前目录文件
@path/to/file       # 指定路径文件
@./relative/path    # 显式相对路径
@/absolute/path     # 绝对路径
```

### 多文件引用

```
@*.ts               # 所有 TypeScript 文件
@src/**/*.js        # src 下所有 JS 文件
@**/*.test.ts       # 所有测试文件
@{file1,file2}      # 多个指定文件
```

### 文件夹引用

```
@src/               # src 目录
@components/**      # components 及其子目录
@docs/*             # docs 直接子项（不递归）
```

## 输出控制

### 格式选项

```
# 代码块
请用代码块展示

# 表格
用表格形式列出

# 列表
以列表形式展示

# JSON
输出为 JSON 格式

# Markdown
生成 Markdown 文档
```

### 详细程度

```
# 简洁模式
简要回答
只给出代码
不要解释

# 详细模式
详细解释
包含注释
提供背景信息

# 逐步模式
分步骤说明
展示思考过程
列出备选方案
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | API 密钥 | - |
| `ANTHROPIC_MODEL` | 默认模型 | claude-sonnet-4-20250514 |
| `CLAUDE_CONFIG` | 配置文件路径 | ~/.claude/config.json |
| `CLAUDE_MAX_TOKENS` | 最大 token 数 | 8192 |
| `CLAUDE_TIMEOUT` | 超时时间 (ms) | 300000 |
| `HTTPS_PROXY` | HTTPS 代理 | - |
| `NO_COLOR` | 禁用颜色输出 | - |

## 退出代码

| 代码 | 说明 |
|------|------|
| 0 | 成功执行 |
| 1 | 一般错误 |
| 2 | 配置错误 |
| 3 | API 错误 |
| 4 | 网络错误 |
| 130 | 用户中断 (Ctrl+C) |

---

**提示**: 使用 `claude --help` 查看最新的命令列表和选项。
