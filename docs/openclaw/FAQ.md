# OpenClaw 常见问题 (FAQ)

常见问题和解决方案汇总。

## 📑 目录

- [安装问题](#安装问题)
- [配置问题](#配置问题)
- [运行问题](#运行问题)
- [Agent 问题](#agent-问题)
- [技能问题](#技能问题)
- [工具问题](#工具问题)
- [性能问题](#性能问题)
- [安全问题](#安全问题)

---

## 安装问题

### Q: 安装时提示权限错误

**问题**: `npm install -g openclaw` 失败，显示权限错误。

**解决方案**:

**Windows**:
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
npm install -g openclaw --force
```

**macOS/Linux**:
```bash
# 方法 1: 使用 sudo
sudo npm install -g openclaw --unsafe-perm=true

# 方法 2: 修复 npm 权限（推荐）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g openclaw
```

### Q: Node.js 版本不兼容

**问题**: 提示 Node.js 版本过低。

**解决方案**:
```bash
# 检查当前版本
node --version

# 使用 nvm 升级（推荐）
nvm install 20
nvm use 20
nvm alias default 20

# 或从官网下载
# https://nodejs.org
```

### Q: 安装后找不到命令

**问题**: 安装成功但 `openclaw` 命令不存在。

**解决方案**:
```bash
# 检查 npm 全局路径
npm bin -g

# 添加到 PATH
# Windows
setx PATH "%PATH%;C:\Users\YourName\AppData\Roaming\npm"

# macOS/Linux
export PATH=$(npm bin -g):$PATH
echo 'export PATH=$(npm bin -g):$PATH' >> ~/.bashrc

# 验证
openclaw --version
```

---

## 配置问题

### Q: API Key 配置无效

**问题**: 模型调用失败，提示认证错误。

**解决方案**:

1. **检查 API Key 格式**:
```json
{
  "models": {
    "providers": {
      "qwen": {
        "apiKey": "sk-正确格式"  // 确保没有多余空格
      }
    }
  }
}
```

2. **使用环境变量**:
```bash
export QWEN_API_KEY="sk-xxx"
```

3. **验证 Key 有效性**:
```bash
curl -H "Authorization: Bearer sk-xxx" \
  https://dashscope.aliyuncs.com/api/v1/models
```

4. **检查配额**:
登录对应平台查看 API 配额和余额。

### Q: 配置文件不生效

**问题**: 修改配置后没有效果。

**解决方案**:
```bash
# 1. 验证配置语法
openclaw config validate

# 2. 重启 Gateway
openclaw gateway restart

# 3. 清除缓存
openclaw system cleanup --cache

# 4. 检查配置路径
# 应该是 ~/.openclaw/config.json
```

### Q: 如何切换模型提供商

**问题**: 想从 Qwen 切换到 Claude。

**解决方案**:

编辑 `~/.openclaw/config.json`:
```json
{
  "models": {
    "default": "anthropic",  // 更改默认模型
    "providers": {
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}",
        "model": "claude-3-sonnet-20240229"
      }
    }
  }
}
```

然后重启：
```bash
openclaw gateway restart
```

---

## 运行问题

### Q: Gateway 启动失败

**问题**: `openclaw gateway start` 失败。

**解决方案**:

1. **检查端口占用**:
```bash
# Windows
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :3000

# 更改端口
openclaw gateway start --port 3001
```

2. **查看详细错误**:
```bash
openclaw gateway start --verbose
openclaw gateway logs --level debug
```

3. **检查依赖**:
```bash
openclaw system doctor
```

4. **重置 Gateway**:
```bash
openclaw gateway stop --force
openclaw system cleanup
openclaw gateway start
```

### Q: Agent 无响应

**问题**: Agent 启动后不响应消息。

**解决方案**:

1. **检查 Agent 状态**:
```bash
openclaw agent status my-agent
openclaw agent logs my-agent
```

2. **重启 Agent**:
```bash
openclaw agent stop my-agent
openclaw agent run my-agent
```

3. **检查模型连接**:
```bash
openclaw test-model qwen
```

4. **增加超时**:
```json
{
  "models": {
    "providers": {
      "qwen": {
        "timeout": 60000
      }
    }
  }
}
```

### Q: 命令执行卡住

**问题**: 某些命令执行后一直等待。

**解决方案**:

```bash
# 设置超时
openclaw exec "long-command" --timeout 30

# 后台运行
openclaw exec "long-command" --background

# 查看进程
openclaw process list

# 终止进程
openclaw process kill <session-id>
```

---

## Agent 问题

### Q: Agent 记忆丢失

**问题**: 重启后 Agent 不记得之前的对话。

**解决方案**:

1. **检查记忆配置**:
```json
{
  "agents": {
    "defaultMemory": true,
    "autoSave": true
  }
}
```

2. **验证记忆文件**:
```bash
ls -la agents/my-agent/memory/
cat agents/my-agent/memory/MEMORY.md
```

3. **手动保存记忆**:
```bash
openclaw memory save my-agent
```

4. **检查权限**:
```bash
# 确保有写入权限
chmod -R 755 agents/my-agent/memory/
```

### Q: Agent 行为不符合预期

**问题**: Agent 回复风格不对。

**解决方案**:

1. **检查 SOUL.md**:
```bash
cat agents/my-agent/SOUL.md
# 确保人格定义清晰
```

2. **检查 USER.md**:
```bash
cat agents/my-agent/USER.md
# 确保用户信息完整
```

3. **添加示例对话**:
在 SOUL.md 中添加：
```markdown
## 对话示例

用户：你好
助手：你好！我是小助手，有什么可以帮你的吗？😊

用户：帮我写代码
助手：好的！请告诉我具体需求...
```

4. **重新训练上下文**:
```bash
openclaw agent reset-context my-agent
```

### Q: 如何删除 Agent

**问题**: 想删除不需要的 Agent。

**解决方案**:
```bash
# 安全删除
openclaw agent delete my-agent

# 强制删除
openclaw agent delete my-agent --force

# 手动删除
rm -rf agents/my-agent
```

---

## 技能问题

### Q: 技能安装失败

**问题**: `openclaw skills install xxx` 失败。

**解决方案**:

1. **检查网络**:
```bash
openclaw network check
```

2. **使用镜像**:
```json
{
  "skills": {
    "clawhub": {
      "registry": "https://mirror.clawhub.com"
    }
  }
}
```

3. **手动安装**:
```bash
git clone https://github.com/xxx/skill-name.git
openclaw skills install ./skill-name
```

4. **检查兼容性**:
```bash
openclaw skills info skill-name
# 查看要求的 OpenClaw 版本
```

### Q: 技能不工作

**问题**: 安装的技能无法使用。

**解决方案**:

1. **检查启用状态**:
```bash
openclaw skills list
openclaw skills enable skill-name
```

2. **查看技能日志**:
```bash
openclaw skills logs skill-name
```

3. **检查配置**:
```bash
cat skills/skill-name/SKILL.md
# 确认配置正确
```

4. **重新安装**:
```bash
openclaw skills uninstall skill-name
openclaw skills install skill-name
```

### Q: 如何开发自定义技能

**问题**: 想创建自己的技能。

**解决方案**:

查看 [Agent 开发指南](AGENT_DEV.md#技能开发)

快速开始：
```bash
openclaw skills create my-skill
cd skills/my-skill
# 编辑 SKILL.md 和 index.js
openclaw skills test my-skill
```

---

## 工具问题

### Q: 浏览器无法启动

**问题**: 浏览器工具报错。

**解决方案**:

1. **安装依赖**:
```bash
# Playwright 浏览器
npx playwright install

# 或 Puppeteer
npm install puppeteer
```

2. **检查配置**:
```json
{
  "tools": {
    "browser": {
      "enabled": true,
      "headless": true
    }
  }
}
```

3. **测试浏览器**:
```bash
openclaw browser open https://example.com
```

4. **使用系统浏览器**:
```json
{
  "tools": {
    "browser": {
      "useSystem": true,
      "path": "/usr/bin/google-chrome"
    }
  }
}
```

### Q: 网络搜索失败

**问题**: web_search 返回错误。

**解决方案**:

1. **检查 API Key**:
```bash
echo $BRAVE_API_KEY
# 或检查配置中的 key
```

2. **测试 API**:
```bash
curl -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=test"
```

3. **检查配额**:
登录 Brave Search 控制台查看使用量。

4. **使用备用方案**:
```json
{
  "tools": {
    "webSearch": {
      "provider": "duckduckgo"  // 或其他提供商
    }
  }
}
```

### Q: 消息发送失败

**问题**: 无法发送消息到 Discord/Telegram 等。

**解决方案**:

1. **检查 Token**:
```bash
# Discord
curl -H "Authorization: Bot $DISCORD_TOKEN" \
  https://discord.com/api/users/@me

# Telegram
curl "https://api.telegram.org/bot$TELEGRAM_TOKEN/getMe"
```

2. **检查权限**:
确保 Bot 有发送消息的权限。

3. **检查频道 ID**:
```bash
# Discord
openclaw message list --channel general
# 确认频道存在
```

4. **查看速率限制**:
某些平台有发送频率限制。

---

## 性能问题

### Q: Agent 响应慢

**问题**: Agent 回复很慢。

**解决方案**:

1. **优化模型参数**:
```json
{
  "models": {
    "providers": {
      "qwen": {
        "maxTokens": 2048,  // 减少最大 token
        "temperature": 0.7
      }
    }
  }
}
```

2. **减少上下文**:
```json
{
  "agents": {
    "maxContextLength": 4096  // 减少上下文长度
  }
}
```

3. **使用更快的模型**:
```json
{
  "models": {
    "default": "qwen-turbo"  // 使用快速版本
  }
}
```

4. **启用缓存**:
```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600
  }
}
```

### Q: 内存占用高

**问题**: OpenClaw 占用大量内存。

**解决方案**:

```bash
# 1. 限制并发 Agent
openclaw config edit
# 设置 maxConcurrent: 3

# 2. 清理缓存
openclaw system cleanup --cache

# 3. 重启服务
openclaw gateway restart

# 4. 检查内存泄漏
openclaw system doctor --full
```

### Q: 磁盘空间不足

**问题**: 日志和记忆占用太多空间。

**解决方案**:

```bash
# 清理旧日志
openclaw system cleanup --logs --older-than 7d

# 清理旧记忆
openclaw memory cleanup --older-than 30d

# 压缩旧文件
find ~/.openclaw/logs -name "*.log" -mtime +7 -exec gzip {} \;

# 设置自动清理
{
  "logging": {
    "maxFiles": 10,
    "maxSize": "10MB"
  }
}
```

---

## 安全问题

### Q: 如何保护 API Key

**问题**: 担心 API Key 泄露。

**解决方案**:

1. **使用环境变量**:
```bash
export QWEN_API_KEY="sk-xxx"
# 在配置中引用 ${QWEN_API_KEY}
```

2. **使用密钥管理**:
```bash
# Linux
echo "sk-xxx" | secret-tool store --label='OpenClaw' openclaw api-key

# macOS
security add-generic-password -s openclaw -a api-key -w "sk-xxx"
```

3. **限制权限**:
```bash
chmod 600 ~/.openclaw/config.json
```

4. **定期轮换**:
定期更新 API Key。

### Q: 如何限制 Agent 权限

**问题**: 防止 Agent 执行危险操作。

**解决方案**:

```json
{
  "security": {
    "requireApproval": [
      "exec",
      "file.delete",
      "message.send"
    ],
    "denylist": [
      "exec.sudo",
      "file.delete_recursive"
    ],
    "allowlist": [
      "read",
      "write",
      "web_search"
    ]
  }
}
```

### Q: 如何审计 Agent 行为

**问题**: 想查看 Agent 做了什么。

**解决方案**:

```bash
# 查看操作日志
openclaw logs agent my-agent --level info

# 导出审计日志
openclaw audit export --output audit.json

# 实时监控
openclaw logs agent my-agent --follow
```

---

## 其他问题

### Q: 如何更新 OpenClaw

**问题**: 想升级到最新版本。

**解决方案**:
```bash
# 检查更新
openclaw system update --check

# 执行更新
openclaw system update

# 或手动更新
npm update -g openclaw

# 验证版本
openclaw --version
```

### Q: 如何备份数据

**问题**: 想备份 Agent 和配置。

**解决方案**:
```bash
# 创建备份
openclaw system backup --output backup-$(date +%Y%m%d).zip

# 或手动备份
tar -czf openclaw-backup.tar.gz \
  ~/.openclaw/config.json \
  ~/openclaw-workspace/agents/
```

### Q: 如何获取帮助

**问题**: 遇到未列出的问题。

**解决方案**:

1. **查看文档**:
```bash
openclaw help
openclaw docs
```

2. **运行诊断**:
```bash
openclaw system doctor --full
```

3. **查看日志**:
```bash
openclaw gateway logs --level debug
```

4. **社区支持**:
- [GitHub Issues](https://github.com/openclaw/issues)
- [Discord 社区](https://discord.gg/openclaw)
- [ClawHub 论坛](https://clawhub.com/forum)

5. **提交 Bug**:
```bash
openclaw bug-report
```

---

## 快速诊断命令

```bash
# 完整系统检查
openclaw system doctor --full

# 检查配置
openclaw config validate

# 测试模型
openclaw test-model qwen

# 检查网络
openclaw network check

# 查看状态
openclaw gateway status
openclaw agent status all

# 清理系统
openclaw system cleanup --all
```

---

**仍有问题？** 请查看完整 [文档](README.md) 或联系社区支持。
