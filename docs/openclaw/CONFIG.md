# OpenClaw 配置说明

详细的配置选项和最佳实践。

## 📁 配置文件位置

```
~/.openclaw/
├── config.json          # 主配置文件
├── agents/              # Agent 配置
├── skills/              # 技能配置
├── memory/              # 记忆存储
└── logs/                # 日志文件
```

## 🔧 主配置文件

### config.json 结构

```json
{
  "version": "1.0",
  "gateway": {
    "port": 3000,
    "host": "localhost",
    "cors": true,
    "ssl": false
  },
  "models": {
    "default": "qwen",
    "fallback": "anthropic",
    "providers": {
      "qwen": {
        "apiKey": "${QWEN_API_KEY}",
        "endpoint": "https://dashscope.aliyuncs.com",
        "model": "qwen-plus",
        "maxTokens": 4096,
        "temperature": 0.7
      },
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}",
        "model": "claude-3-sonnet-20240229",
        "maxTokens": 4096
      },
      "openai": {
        "apiKey": "${OPENAI_API_KEY}",
        "model": "gpt-4-turbo",
        "maxTokens": 4096
      }
    }
  },
  "agents": {
    "defaultMemory": true,
    "autoSave": true,
    "maxContextLength": 8192
  },
  "skills": {
    "autoUpdate": false,
    "clawhub": {
      "enabled": true,
      "registry": "https://clawhub.com"
    }
  },
  "tools": {
    "browser": {
      "enabled": true,
      "headless": true,
      "timeout": 30000
    },
    "webSearch": {
      "enabled": true,
      "provider": "brave",
      "apiKey": "${BRAVE_API_KEY}"
    },
    "message": {
      "enabled": true,
      "platforms": ["discord", "telegram"]
    }
  },
  "security": {
    "requireApproval": ["exec", "message"],
    "allowlist": ["read", "write", "web_search"],
    "rateLimit": {
      "enabled": true,
      "requestsPerMinute": 60
    }
  },
  "logging": {
    "level": "info",
    "format": "json",
    "output": "file",
    "maxFiles": 10,
    "maxSize": "10MB"
  },
  "workspace": {
    "path": "~/openclaw-workspace",
    "autoCreate": true
  }
}
```

## 🤖 模型配置

### 基础配置

```json
{
  "models": {
    "default": "qwen",
    "providers": {
      "qwen": {
        "apiKey": "sk-xxx",
        "endpoint": "https://dashscope.aliyuncs.com",
        "model": "qwen-plus",
        "maxTokens": 4096,
        "temperature": 0.7,
        "topP": 0.9,
        "frequencyPenalty": 0.5,
        "presencePenalty": 0.5,
        "timeout": 30000,
        "retryAttempts": 3
      }
    }
  }
}
```

### 多模型配置

```json
{
  "models": {
    "default": "qwen",
    "fallback": "anthropic",
    "routing": {
      "coding": "qwen",
      "creative": "anthropic",
      "analysis": "openai"
    },
    "providers": {
      "qwen": {
        "apiKey": "${QWEN_API_KEY}",
        "model": "qwen-plus"
      },
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}",
        "model": "claude-3-sonnet-20240229"
      },
      "openai": {
        "apiKey": "${OPENAI_API_KEY}",
        "model": "gpt-4-turbo"
      }
    }
  }
}
```

### 模型参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `temperature` | 创造性（0-1） | 0.7 |
| `topP` | 采样概率（0-1） | 0.9 |
| `maxTokens` | 最大 token 数 | 4096 |
| `timeout` | 超时时间（ms） | 30000 |
| `retryAttempts` | 重试次数 | 3 |
| `frequencyPenalty` | 频率惩罚 | 0.5 |
| `presencePenalty` | 存在惩罚 | 0.5 |

## 🛠️ 工具配置

### 浏览器工具

```json
{
  "tools": {
    "browser": {
      "enabled": true,
      "headless": true,
      "timeout": 30000,
      "proxy": null,
      "userDataDir": "~/.openclaw/browser-data",
      "extensions": [],
      "preferences": {
        "defaultViewport": {
          "width": 1920,
          "height": 1080
        }
      }
    }
  }
}
```

### 网络搜索

```json
{
  "tools": {
    "webSearch": {
      "enabled": true,
      "provider": "brave",
      "apiKey": "${BRAVE_API_KEY}",
      "maxResults": 10,
      "safeSearch": true,
      "country": "US",
      "language": "en"
    }
  }
}
```

### 消息工具

```json
{
  "tools": {
    "message": {
      "enabled": true,
      "platforms": {
        "discord": {
          "enabled": true,
          "token": "${DISCORD_TOKEN}",
          "guildId": "xxx",
          "channels": ["general", "bot-commands"]
        },
        "telegram": {
          "enabled": true,
          "token": "${TELEGRAM_TOKEN}",
          "allowedUsers": ["username1", "username2"]
        },
        "feishu": {
          "enabled": true,
          "appId": "${FEISHU_APP_ID}",
          "appSecret": "${FEISHU_APP_SECRET}",
          "encryptKey": "${FEISHU_ENCRYPT_KEY}"
        }
      }
    }
  }
}
```

### Feishu 集成

```json
{
  "tools": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "xxx",
      "verificationToken": "xxx",
      "botName": "OpenClaw Bot",
      "permissions": {
        "docs": true,
        "drive": true,
        "wiki": true,
        "chat": true,
        "bitable": true
      }
    }
  }
}
```

## 🔒 安全配置

### 权限控制

```json
{
  "security": {
    "requireApproval": [
      "exec",
      "message.send",
      "browser.navigate",
      "file.delete"
    ],
    "allowlist": [
      "read",
      "write",
      "web_search",
      "web_fetch"
    ],
    "denylist": [
      "exec.sudo",
      "file.delete_recursive"
    ],
    "rateLimit": {
      "enabled": true,
      "requestsPerMinute": 60,
      "requestsPerHour": 1000
    },
    "ipWhitelist": [
      "127.0.0.1",
      "192.168.1.0/24"
    ]
  }
}
```

### SSL/TLS 配置

```json
{
  "gateway": {
    "ssl": true,
    "sslOptions": {
      "key": "/path/to/private.key",
      "cert": "/path/to/certificate.crt",
      "ca": "/path/to/ca.crt"
    },
    "redirectHttp": true,
    "minTlsVersion": "TLSv1.2"
  }
}
```

## 📝 Agent 配置

### Agent 基础配置

```json
{
  "agents": {
    "defaultMemory": true,
    "autoSave": true,
    "maxContextLength": 8192,
    "sessionTimeout": 3600,
    "maxConcurrent": 5,
    "defaultSkills": [
      "file-ops",
      "web-search",
      "browser"
    ]
  }
}
```

### Agent 个性化

每个 Agent 有自己的配置文件：

```json
{
  "name": "my-assistant",
  "model": "qwen",
  "personality": {
    "name": "小助手",
    "tone": "friendly",
    "language": "zh-CN"
  },
  "capabilities": [
    "coding",
    "writing",
    "analysis"
  ],
  "restrictions": {
    "maxTokensPerRequest": 4096,
    "allowedDomains": ["github.com", "stackoverflow.com"]
  },
  "memory": {
    "enabled": true,
    "maxSize": 1000,
    "persistence": true
  }
}
```

## 🎯 技能配置

### 技能管理

```json
{
  "skills": {
    "autoUpdate": false,
    "autoEnable": true,
    "clawhub": {
      "enabled": true,
      "registry": "https://clawhub.com",
      "autoSync": false,
      "syncInterval": 86400
    },
    "installed": [
      {
        "name": "weather",
        "version": "1.2.0",
        "enabled": true,
        "config": {
          "apiKey": "${WEATHER_API_KEY}",
          "units": "metric"
        }
      },
      {
        "name": "github-tools",
        "version": "2.0.1",
        "enabled": true,
        "config": {
          "token": "${GITHUB_TOKEN}"
        }
      }
    ]
  }
}
```

## 📊 日志配置

### 日志级别

```json
{
  "logging": {
    "level": "info",
    "format": "json",
    "output": "file",
    "maxFiles": 10,
    "maxSize": "10MB",
    "compress": true,
    "timestamp": true,
    "colors": false
  }
}
```

### 日志级别说明

| 级别 | 说明 | 使用场景 |
|------|------|---------|
| `error` | 错误信息 | 生产环境 |
| `warn` | 警告信息 | 生产环境 |
| `info` | 一般信息 | 默认 |
| `debug` | 调试信息 | 开发环境 |
| `trace` | 详细追踪 | 深度调试 |

## 🌐 网络配置

### 代理配置

```json
{
  "network": {
    "proxy": {
      "enabled": true,
      "http": "http://proxy.example.com:8080",
      "https": "http://proxy.example.com:8080",
      "noProxy": ["localhost", "127.0.0.1"]
    },
    "dns": {
      "servers": ["8.8.8.8", "8.8.4.4"]
    },
    "timeout": {
      "connect": 10000,
      "read": 30000,
      "write": 30000
    }
  }
}
```

## 💾 存储配置

### 本地存储

```json
{
  "storage": {
    "type": "local",
    "path": "~/.openclaw/data",
    "maxSize": "1GB",
    "cleanup": {
      "enabled": true,
      "interval": 86400,
      "maxAge": 2592000
    }
  }
}
```

### 远程存储

```json
{
  "storage": {
    "type": "s3",
    "bucket": "openclaw-data",
    "region": "us-east-1",
    "accessKeyId": "${AWS_ACCESS_KEY}",
    "secretAccessKey": "${AWS_SECRET_KEY}",
    "prefix": "openclaw/"
  }
}
```

## 🔔 通知配置

```json
{
  "notifications": {
    "enabled": true,
    "channels": {
      "email": {
        "enabled": false,
        "smtp": {
          "host": "smtp.example.com",
          "port": 587,
          "user": "${SMTP_USER}",
          "password": "${SMTP_PASSWORD}"
        },
        "recipients": ["admin@example.com"]
      },
      "webhook": {
        "enabled": true,
        "url": "${WEBHOOK_URL}",
        "events": ["error", "warning"]
      }
    }
  }
}
```

## 🎛️ 环境变量

使用环境变量管理敏感信息：

```bash
# .env 文件
QWEN_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-proj-xxx
DISCORD_TOKEN=xxx
TELEGRAM_TOKEN=xxx
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
BRAVE_API_KEY=xxx
AWS_ACCESS_KEY=xxx
AWS_SECRET_KEY=xxx
```

在配置中引用：

```json
{
  "models": {
    "providers": {
      "qwen": {
        "apiKey": "${QWEN_API_KEY}"
      }
    }
  }
}
```

## ✅ 配置验证

```bash
# 验证配置文件
openclaw config validate

# 检查配置问题
openclaw doctor

# 测试模型连接
openclaw test-model qwen
```

## 📋 配置模板

### 开发环境

```json
{
  "gateway": {
    "port": 3000,
    "host": "localhost"
  },
  "logging": {
    "level": "debug"
  },
  "security": {
    "requireApproval": []
  }
}
```

### 生产环境

```json
{
  "gateway": {
    "port": 443,
    "ssl": true
  },
  "logging": {
    "level": "warn"
  },
  "security": {
    "requireApproval": ["exec", "message.send"],
    "rateLimit": {
      "enabled": true,
      "requestsPerMinute": 30
    }
  }
}
```

---

**提示**: 修改配置后重启 Gateway 使更改生效：`openclaw gateway restart`
