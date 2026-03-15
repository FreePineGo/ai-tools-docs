# OpenClaw 安装指南

本指南将帮助你完成 OpenClaw 的完整安装和配置。

## 📋 前置要求

### 系统要求

- **操作系统**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Node.js**: v18.0 或更高版本（推荐 v20+）
- **npm**: v8.0 或更高版本
- **存储空间**: 至少 500MB 可用空间

### 检查 Node.js 版本

```bash
node --version
npm --version
```

如果版本过低，请前往 [Node.js 官网](https://nodejs.org) 下载最新版本。

## 🔧 安装步骤

### 方法一：全局安装（推荐）

```bash
# 使用 npm 全局安装
npm install -g openclaw

# 验证安装
openclaw --version
```

### 方法二：使用 yarn

```bash
yarn global add openclaw

# 验证安装
openclaw --version
```

### 方法三：从源码安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安装依赖
npm install

# 链接到全局
npm link
```

## 🌍 平台特定安装

### Windows

```powershell
# 以管理员身份运行 PowerShell
npm install -g openclaw

# 如果遇到权限问题
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
npm install -g openclaw
```

### macOS

```bash
# 如果遇到权限问题
sudo npm install -g openclaw --unsafe-perm=true

# 或使用 nvm (推荐)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
npm install -g openclaw
```

### Linux (Ubuntu/Debian)

```bash
# 安装 Node.js (如果未安装)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 OpenClaw
sudo npm install -g openclaw
```

### Raspberry Pi

```bash
# 确保系统更新
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 OpenClaw
sudo npm install -g openclaw
```

## ⚙️ 初始配置

### 1. 初始化工作空间

```bash
# 创建工作空间目录
mkdir -p ~/openclaw-workspace
cd ~/openclaw-workspace

# 初始化 OpenClaw
openclaw init
```

### 2. 配置 AI 模型

创建或编辑配置文件 `~/.openclaw/config.json`:

```json
{
  "models": {
    "default": "qwen",
    "providers": {
      "qwen": {
        "apiKey": "your-qwen-api-key",
        "endpoint": "https://dashscope.aliyuncs.com"
      },
      "anthropic": {
        "apiKey": "your-anthropic-api-key"
      },
      "openai": {
        "apiKey": "your-openai-api-key"
      }
    }
  }
}
```

### 3. 配置环境变量（可选）

```bash
# Linux/macOS
export OPENCLAW_API_KEY="your-api-key"
export OPENCLAW_WORKSPACE="~/openclaw-workspace"

# Windows PowerShell
$env:OPENCLAW_API_KEY="your-api-key"
$env:OPENCLAW_WORKSPACE="~/openclaw-workspace"
```

## 🚀 启动网关

```bash
# 启动 Gateway 服务
openclaw gateway start

# 检查状态
openclaw gateway status

# 查看日志
openclaw gateway logs
```

## ✅ 验证安装

运行以下命令验证安装是否成功：

```bash
# 检查版本
openclaw --version

# 查看帮助
openclaw --help

# 列出可用命令
openclaw help

# 检查网关状态
openclaw gateway status
```

## 🔍 故障排除

### 常见问题

#### 1. 权限错误

**Windows**:
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux**:
```bash
sudo npm install -g openclaw --unsafe-perm=true
```

#### 2. Node.js 版本过低

```bash
# 使用 nvm 升级 Node.js
nvm install 20
nvm use 20
```

#### 3. 网络连接问题

```bash
# 检查网络配置
openclaw network check

# 配置代理（如果需要）
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

#### 4. 端口被占用

```bash
# 更改网关端口
openclaw gateway start --port 3001

# 或查看占用端口的进程
# Windows
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :3000
```

### 获取帮助

```bash
# 查看完整帮助
openclaw help

# 查看特定命令帮助
openclaw gateway --help

# 报告问题
openclaw bug-report
```

## 📚 下一步

安装完成后，请查看：

- [快速开始](QUICKSTART.md) - 5 分钟上手指南
- [命令参考](COMMANDS.md) - 完整命令列表
- [配置说明](CONFIG.md) - 详细配置选项

---

**需要帮助？** 访问 [常见问题](FAQ.md) 或加入我们的 [Discord 社区](https://discord.gg/openclaw)
