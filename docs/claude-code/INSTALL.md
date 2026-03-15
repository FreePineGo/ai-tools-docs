# Claude Code 安装指南

## 前置要求

在开始安装之前，请确保满足以下要求：

### 系统要求

| 组件 | 要求 | 验证命令 |
|------|------|----------|
| Node.js | v18.0+ | `node --version` |
| npm | v9.0+ | `npm --version` |
| 操作系统 | macOS 10.15+ / Linux / Windows 10+ | - |

### 安装 Node.js

#### macOS

```bash
# 使用 Homebrew (推荐)
brew install node

# 或使用官方安装包
# 访问 https://nodejs.org 下载 LTS 版本
```

#### Linux

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs

# 或使用 nvm (推荐)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

#### Windows

1. 访问 [https://nodejs.org](https://nodejs.org)
2. 下载 LTS 版本安装程序
3. 运行安装程序，按提示完成安装
4. 重启终端验证：`node --version`

## 安装步骤

### 步骤 1: 全局安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

**注意**: 如果遇到权限问题：

```bash
# macOS/Linux: 使用 sudo
sudo npm install -g @anthropic-ai/claude-code

# 或者修改 npm 默认目录 (推荐)
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

### 步骤 2: 验证安装

```bash
claude --version
```

成功输出示例：
```
claude-code/1.0.0 (node/v20.x.x)
```

### 步骤 3: 配置 API 密钥

#### 方法一：交互式配置（推荐）

```bash
claude
```

首次运行时，会提示输入 API 密钥。

#### 方法二：环境变量

```bash
# macOS/Linux (~/.bashrc 或 ~/.zshrc)
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"

# Windows CMD
set ANTHROPIC_API_KEY=your-api-key-here
```

#### 方法三：配置文件

创建 `~/.claude/config.json`:

```json
{
  "apiKey": "your-api-key-here",
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 8192
}
```

### 步骤 4: 获取 API 密钥

1. 访问 [https://console.anthropic.com](https://console.anthropic.com)
2. 登录或注册账户
3. 进入 API Keys 页面
4. 创建新的 API 密钥
5. 复制密钥并保存（只显示一次）

#### API 密钥类型

| 类型 | 用途 | 配额 |
|------|------|------|
| Free Tier | 个人试用 | 有限额度 |
| Paid Tier | 生产使用 | 根据套餐 |
| Enterprise | 企业定制 | 联系销售 |

## 验证安装

运行以下命令验证一切正常：

```bash
# 检查版本
claude --version

# 运行测试对话
echo "Hello, Claude! Please respond with 'Installation successful!'" | claude
```

## 可选配置

### 设置默认模型

```bash
# 在配置文件中设置
echo '{"defaultModel": "claude-sonnet-4-20250514"}' >> ~/.claude/config.json
```

### 配置代理（如需要）

```bash
export HTTPS_PROXY="http://proxy-server:port"
export HTTP_PROXY="http://proxy-server:port"
```

### 增加 Token 限制

```json
{
  "maxTokens": 16384,
  "timeout": 300000
}
```

## 故障排除

### 问题 1: npm 安装失败

```bash
# 清除 npm 缓存
npm cache clean --force

# 重新安装
npm install -g @anthropic-ai/claude-code
```

### 问题 2: 权限错误

```bash
# macOS/Linux
sudo chown -R $(whoami) ~/.npm

# 或使用 nvm 避免权限问题
nvm install --lts
```

### 问题 3: API 密钥无效

- 检查密钥是否正确复制（无多余空格）
- 确认账户有可用额度
- 检查网络连接
- 验证 API 端点是否正确

### 问题 4: 命令未找到

```bash
# 检查 PATH
echo $PATH

# 找到 claude 安装位置
which claude

# 手动添加到 PATH
export PATH=$PATH:$(npm config get prefix)/bin
```

### 问题 5: 连接超时

```bash
# 检查网络
ping console.anthropic.com

# 检查防火墙设置
# 确保允许访问 API 端点
```

## 升级

```bash
# 升级到最新版本
npm update -g @anthropic-ai/claude-code

# 或重新安装
npm install -g @anthropic-ai/claude-code@latest
```

## 卸载

```bash
npm uninstall -g @anthropic-ai/claude-code

# 清理配置文件
rm -rf ~/.claude
```

---

安装完成后，请继续阅读 [QUICKSTART.md](./QUICKSTART.md) 开始使用。
