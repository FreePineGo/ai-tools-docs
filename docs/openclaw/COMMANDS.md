# OpenClaw 命令参考

完整的 OpenClaw 命令列表和使用示例。

## 📑 目录

- [全局命令](#全局命令)
- [Gateway 命令](#gateway-命令)
- [Agent 命令](#agent-命令)
- [文件命令](#文件命令)
- [网络命令](#网络命令)
- [浏览器命令](#浏览器命令)
- [消息命令](#消息命令)
- [技能命令](#技能命令)
- [记忆命令](#记忆命令)
- [系统命令](#系统命令)

---

## 全局命令

### `openclaw --version`

显示 OpenClaw 版本号。

```bash
openclaw --version
# 输出：1.0.0
```

### `openclaw --help`

显示帮助信息。

```bash
openclaw --help
openclaw -h
```

### `openclaw help [command]`

显示特定命令的帮助。

```bash
openclaw help gateway
openclaw help agent create
```

### `openclaw init`

初始化新的工作空间。

```bash
openclaw init
openclaw init --name my-workspace
openclaw init --template default
```

### `openclaw config`

管理配置文件。

```bash
openclaw config view          # 查看配置
openclaw config edit          # 编辑配置
openclaw config reset         # 重置配置
openclaw config validate      # 验证配置
```

---

## Gateway 命令

### `openclaw gateway start`

启动 Gateway 服务。

```bash
openclaw gateway start
openclaw gateway start --port 3001
openclaw gateway start --host 0.0.0.0
openclaw gateway start --daemon  # 后台运行
```

**选项**:
- `--port, -p`: 端口号（默认：3000）
- `--host, -h`: 绑定地址（默认：localhost）
- `--daemon, -d`: 后台运行
- `--verbose, -v`: 详细日志

### `openclaw gateway stop`

停止 Gateway 服务。

```bash
openclaw gateway stop
openclaw gateway stop --force
```

### `openclaw gateway restart`

重启 Gateway 服务。

```bash
openclaw gateway restart
openclaw gateway restart --graceful
```

### `openclaw gateway status`

查看 Gateway 运行状态。

```bash
openclaw gateway status
openclaw gateway status --json
```

### `openclaw gateway logs`

查看 Gateway 日志。

```bash
openclaw gateway logs
openclaw gateway logs --follow      # 实时跟踪
openclaw gateway logs --lines 100   # 显示行数
openclaw gateway logs --level error # 过滤级别
```

### `openclaw gateway health`

运行健康检查。

```bash
openclaw gateway health
openclaw gateway health --full
```

---

## Agent 命令

### `openclaw agent list`

列出所有 Agent。

```bash
openclaw agent list
openclaw agent list --status
openclaw agent list --json
```

### `openclaw agent create <name>`

创建新 Agent。

```bash
openclaw agent create my-assistant
openclaw agent create bot --template customer-service
openclaw agent create dev --interactive
```

**选项**:
- `--template, -t`: 使用模板
- `--interactive, -i`: 交互式创建
- `--path, -p`: 自定义路径

### `openclaw agent run <name>`

运行 Agent。

```bash
openclaw agent run my-assistant
openclaw agent run bot --message "你好"
openclaw agent run dev --file task.md
```

**选项**:
- `--message, -m`: 发送消息
- `--file, -f`: 从文件读取任务
- `--interactive, -i`: 交互模式
- `--quiet, -q`: 安静模式

### `openclaw agent stop <name>`

停止运行中的 Agent。

```bash
openclaw agent stop my-assistant
openclaw agent stop all
```

### `openclaw agent status <name>`

查看 Agent 状态。

```bash
openclaw agent status my-assistant
openclaw agent status all
```

### `openclaw agent delete <name>`

删除 Agent。

```bash
openclaw agent delete my-assistant
openclaw agent delete old-bot --force
```

### `openclaw agent export <name>`

导出 Agent 配置。

```bash
openclaw agent export my-assistant
openclaw agent export bot --format json
openclaw agent export all --output backup.zip
```

### `openclaw agent import <file>`

导入 Agent。

```bash
openclaw agent import agent-config.json
openclaw agent import backup.zip
```

---

## 文件命令

### `openclaw file read <path>`

读取文件内容。

```bash
openclaw file read myfile.txt
openclaw file read src/index.js --lines 50
openclaw file read config.json --json
```

**选项**:
- `--lines, -n`: 显示行数
- `--offset, -o`: 起始行
- `--json`: JSON 格式化输出

### `openclaw file write <path> [content]`

写入文件内容。

```bash
openclaw file write hello.txt "Hello World"
openclaw file write config.json --input data.json
openclaw file write output.md --stdin
```

**选项**:
- `--input, -i`: 从文件读取内容
- `--stdin`: 从标准输入读取
- `--append, -a`: 追加模式
- `--force, -f`: 强制覆盖

### `openclaw file edit <path>`

编辑文件。

```bash
openclaw file edit myfile.txt
openclaw file edit config.json --editor vim
```

**选项**:
- `--editor, -e`: 指定编辑器

### `openclaw file list <directory>`

列出目录内容。

```bash
openclaw file list .
openclaw file list src --recursive
openclaw file list docs --pattern "*.md"
```

**选项**:
- `--recursive, -r`: 递归列出
- `--pattern, -p`: 文件模式
- `--long, -l`: 详细信息

### `openclaw file copy <src> <dest>`

复制文件。

```bash
openclaw file copy file.txt backup.txt
openclaw file copy src/ dist/ --recursive
```

### `openclaw file move <src> <dest>`

移动文件。

```bash
openclaw file move old.txt new.txt
openclaw file move temp/ archive/
```

### `openclaw file delete <path>`

删除文件。

```bash
openclaw file delete temp.txt
openclaw file delete old-folder --recursive
openclaw file delete *.log --force
```

---

## 网络命令

### `openclaw web search <query>`

搜索网络。

```bash
openclaw web search "OpenClaw documentation"
openclaw web search "AI news" --count 10
openclaw web search "tutorial" --freshness week
```

**选项**:
- `--count, -n`: 结果数量（默认：10）
- `--freshness, -f`: 时间过滤（day/week/month/year）
- `--language, -l`: 语言代码
- `--country, -c`: 国家代码

### `openclaw web fetch <url>`

获取网页内容。

```bash
openclaw web fetch https://example.com
openclaw web fetch https://example.com --markdown
openclaw web fetch https://example.com --text
```

**选项**:
- `--markdown, -m`: Markdown 格式输出
- `--text, -t`: 纯文本输出
- `--max-chars, -c`: 最大字符数

### `openclaw web download <url>`

下载文件。

```bash
openclaw web download https://example.com/file.pdf
openclaw web download https://example.com/image.jpg --output my-image.jpg
```

---

## 浏览器命令

### `openclaw browser open <url>`

打开浏览器。

```bash
openclaw browser open https://example.com
openclaw browser open --new-tab
openclaw browser open --incognito
```

### `openclaw browser screenshot`

截取屏幕截图。

```bash
openclaw browser screenshot
openclaw browser screenshot --full-page
openclaw browser screenshot --output capture.png
```

### `openclaw browser click <selector>`

点击页面元素。

```bash
openclaw browser click "#submit-button"
openclaw browser click ".nav-item" --index 2
```

### `openclaw browser type <selector> <text>`

输入文本。

```bash
openclaw browser type "#username" "myuser"
openclaw browser type "input[name='email']" "test@example.com"
```

### `openclaw browser evaluate <script>`

执行 JavaScript。

```bash
openclaw browser evaluate "document.title"
openclaw browser evaluate "document.querySelectorAll('.item').length"
```

### `openclaw browser close`

关闭浏览器。

```bash
openclaw browser close
openclaw browser close --all
```

---

## 消息命令

### `openclaw message send <message>`

发送消息。

```bash
openclaw message send "Hello World"
openclaw message send "Task complete" --channel general
openclaw message send "Report" --thread 12345
```

**选项**:
- `--channel, -c`: 目标频道
- `--thread, -t`: 线程 ID
- `--reply-to, -r`: 回复消息 ID
- `--file, -f`: 附加文件

### `openclaw message broadcast <message>`

广播消息。

```bash
openclaw message broadcast "System maintenance in 1 hour"
openclaw message broadcast "Update available" --channels general,announcements
```

### `openclaw message list`

列出消息。

```bash
openclaw message list --channel general
openclaw message list --limit 50
openclaw message list --since "2024-01-01"
```

---

## 技能命令

### `openclaw skills list`

列出可用技能。

```bash
openclaw skills list
openclaw skills list --installed
openclaw skills list --available
```

### `openclaw skills install <name>`

安装技能。

```bash
openclaw skills install weather
openclaw skills install github-tools --version 1.2.0
openclaw skills install ./local-skill
```

### `openclaw skills uninstall <name>`

卸载技能。

```bash
openclaw skills uninstall weather
openclaw skills uninstall old-skill --force
```

### `openclaw skills update [name]`

更新技能。

```bash
openclaw skills update
openclaw skills update weather
openclaw skills update --all
```

### `openclaw skills create <name>`

创建新技能。

```bash
openclaw skills create my-skill
openclaw skills create custom-tool --template basic
```

### `openclaw skills enable <name>`

启用技能。

```bash
openclaw skills enable weather
openclaw skills enable all
```

### `openclaw skills disable <name>`

禁用技能。

```bash
openclaw skills disable weather
openclaw skills disable experimental
```

---

## 记忆命令

### `openclaw memory list`

列出记忆。

```bash
openclaw memory list
openclaw memory list --today
openclaw memory list --agent my-assistant
```

### `openclaw memory add <content>`

添加记忆。

```bash
openclaw memory add "用户偏好使用中文"
openclaw memory add "项目截止日期：2024-12-31" --project my-project
openclaw memory add "重要信息" --priority high
```

### `openclaw memory search <query>`

搜索记忆。

```bash
openclaw memory search "API key"
openclaw memory search "configuration" --agent dev-bot
```

### `openclaw memory delete <id>`

删除记忆。

```bash
openclaw memory delete 12345
openclaw memory delete --older-than 30d
```

### `openclaw memory export`

导出记忆。

```bash
openclaw memory export --format json
openclaw memory export --output backup.json
```

### `openclaw memory import <file>`

导入记忆。

```bash
openclaw memory import backup.json
```

---

## 系统命令

### `openclaw system info`

显示系统信息。

```bash
openclaw system info
openclaw system info --json
```

### `openclaw system doctor`

运行诊断。

```bash
openclaw system doctor
openclaw system doctor --full
```

### `openclaw system update`

更新 OpenClaw。

```bash
openclaw system update
openclaw system update --check
openclaw system update --force
```

### `openclaw system cleanup`

清理缓存。

```bash
openclaw system cleanup
openclaw system cleanup --cache
openclaw system cleanup --logs
openclaw system cleanup --all
```

### `openclaw system backup`

创建备份。

```bash
openclaw system backup
openclaw system backup --output backup-2024.zip
openclaw system backup --include agents,skills,memory
```

### `openclaw system restore <backup>`

恢复备份。

```bash
openclaw system restore backup-2024.zip
openclaw system restore --dry-run backup.zip
```

---

## 快捷键和别名

### 常用别名

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
alias oc='openclaw'
alias ocg='openclaw gateway'
alias oca='openclaw agent'
alias ocf='openclaw file'
alias ocw='openclaw web'
```

### 快捷命令

```bash
# 快速启动
oc start          # openclaw gateway start
oc stop           # openclaw gateway stop
oc run bot        # openclaw agent run bot

# 快速开发
oc new skill      # openclaw skills create
oc new agent      # openclaw agent create
oc edit config    # openclaw config edit
```

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_HOME` | 主目录 | `~/.openclaw` |
| `OPENCLAW_WORKSPACE` | 工作空间 | `~/openclaw-workspace` |
| `OPENCLAW_PORT` | 网关端口 | `3000` |
| `OPENCLAW_LOG_LEVEL` | 日志级别 | `info` |
| `OPENCLAW_API_KEY` | API 密钥 | - |
| `OPENCLAW_DEBUG` | 调试模式 | `false` |

---

## 退出代码

| 代码 | 含义 |
|------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 配置错误 |
| 3 | 网络错误 |
| 4 | 权限错误 |
| 5 | 资源不存在 |

---

**提示**: 使用 `openclaw help <command>` 查看特定命令的详细帮助！
