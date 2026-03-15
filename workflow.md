# AI Publisher Agent - 工作流程定义

## 📋 工作流列表

| 工作流 | 触发条件 | 预期结果 |
|--------|----------|----------|
| `full-publish` | 完整发布流程 | 文章发布到公众号 |
| `generate-only` | 仅生成文章 | 文章保存到草稿 |
| `cover-only` | 仅生成封面 | 封面图保存 |
| `publish-existing` | 发布已有草稿 | 文章发布到公众号 |
| `check-status` | 查询状态 | 返回当前状态 |

---

## 🔄 工作流 1: full-publish (完整发布)

### 触发指令
- "发布今天的 AI 文章"
- "发公众号"
- "搞定今天的资讯"
- "publish article"

### 流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                     full-publish 工作流                          │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────────────┐
  │ START            │
  └────────┬─────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 1: 意图确认                                                │
  │ - 识别用户指令                                                  │
  │ - 确定目标：发布今日 AI 文章到公众号                              │
  │ - 初始化执行状态                                                │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 2: 检查文章状态                                            │
  │ - 调用 get-latest-article                                       │
  │ - IF 文章存在 AND 是今日 → Step 3                              │
  │ - IF 文章不存在 OR 不是今日 → 调用 generate-article            │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 3: 检查封面图状态                                          │
  │ - 调用 check-file-exists (cover-{date}.png)                    │
  │ - IF 封面存在 → Step 4                                         │
  │ - IF 封面不存在 → 调用 generate-cover                          │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 4: 检查浏览器环境                                          │
  │ - 调用 check-browser-status                                     │
  │ - IF connected=true AND cdpReady=true → Step 5                │
  │ - IF NOT connected → notify-user 并等待                        │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 5: 检查公众号登录状态                                      │
  │ - 调用 navigate-browser (mp.weixin.qq.com)                     │
  │ - 调用 browser-snapshot 检查页面元素                            │
  │ - IF 已登录 → Step 6                                           │
  │ - IF 未登录 → 等待用户扫码后继续                               │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 6: 执行发布操作                                            │
  │ - 导航到编辑器页面                                              │
  │ - 点击"新的创作" → "写文章"                                    │
  │ - 填写标题（browser-type）                                      │
  │ - 粘贴内容（browser-type）                                      │
  │ - 上传封面图                                                    │
  │ - 点击"群发"按钮                                               │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 7: 确认发布结果                                            │
  │ - 检查发布状态                                                  │
  │ - IF 成功 → Step 8                                             │
  │ - IF 失败 → 错误处理流程                                       │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────┐
  │ Step 8: 记录与通知                                              │
  │ - 调用 update-memory 更新状态                                   │
  │ - 调用 log-execution 记录日志                                   │
  │ - 调用 notify-user 通知用户完成                                 │
  └────────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌──────────────────┐
  │ END (SUCCESS)    │
  └──────────────────┘
```

### 状态变量

```json
{
  "workflow": "full-publish",
  "status": "running | completed | failed",
  "current_step": 1-8,
  "variables": {
    "article_path": "string",
    "article_title": "string",
    "cover_path": "string",
    "cover_style": "string",
    "browser_tab_id": "string",
    "publish_url": "string"
  },
  "errors": [],
  "start_time": "datetime",
  "end_time": "datetime"
}
```

### 错误处理

| 错误 | 处理策略 |
|------|----------|
| 文章生成失败 | 重试 1 次 → 通知用户 |
| 封面生成失败 | 切换风格重试 → 使用旧封面 |
| 浏览器未连接 | 提示用户激活 → 等待 60 秒 → 重试 |
| 公众号未登录 | 导航到登录页 → 等待扫码 → 超时通知 |
| 发布失败 | 保存草稿 → 通知用户手动处理 |

---

## 📝 工作流 2: generate-only (仅生成文章)

### 触发指令
- "生成今天的 AI 资讯"
- "ai news"
- "今日资讯"

### 流程

```
START → generate-article → check-ai-detection → 
IF passed → save → notify → END
IF failed → optimize → retry detection → ...
```

### 输出
- 文章文件路径
- AI 检测报告
- 标题和字数统计

---

## 🖼️ 工作流 3: cover-only (仅生成封面)

### 触发指令
- "生成封面"
- "生成公众号封面"
- "生成今天封面"

### 流程

```
START → get-latest-article → extract-title → 
generate-cover → save → notify → END
```

### 参数
- `style`: 封面风格（可选，默认 auto）
- `date`: 日期（可选，默认今天）

---

## 📤 工作流 4: publish-existing (发布已有草稿)

### 触发指令
- "发布 AI 文章"
- "发布草稿"
- "用最新草稿发布"

### 流程

```
START → get-latest-article → check-cover → 
check-browser → check-wechat-login → publish → notify → END
```

### 与 full-publish 的区别
- 跳过文章生成步骤
- 直接使用已有草稿

---

## 📊 工作流 5: check-status (查询状态)

### 触发指令
- "发布状态"
- "今天发布了吗"
- "检查状态"

### 流程

```
START → get-memory → 
check-article → check-cover → check-browser → 
compile-status → notify → END
```

### 输出格式

```markdown
## 📊 发布状态

| 项目 | 状态 |
|------|------|
| 今日文章 | ✅ 已生成 |
| 封面图 | ✅ 已生成 (科技风格) |
| 浏览器 | ✅ 已连接 |
| 公众号 | ⏳ 待发布 |

**下一步：** 执行发布操作
```

---

## 🧩 子流程：错误恢复

### 浏览器连接问题

```
ERROR: browser not connected
  ↓
notify-user: "请激活浏览器扩展"
  ↓
wait: 60 seconds
  ↓
retry: check-browser-status
  ↓
IF success → continue
IF failed → notify-user: "无法连接浏览器，建议手动发布"
```

### 公众号登录问题

```
ERROR: wechat not logged in
  ↓
navigate: mp.weixin.qq.com
  ↓
notify-user: "请扫码登录公众号"
  ↓
poll: check-login-status (every 5s, max 120s)
  ↓
IF logged in → continue
IF timeout → notify-user: "登录超时，请重试"
```

### AI 检测超标

```
ERROR: AI percentage > 10%
  ↓
optimize-article:
  - 打散句子结构
  - 加入情感词
  - 添加主观评价
  - 使用人称代词
  ↓
retry: check-ai-detection
  ↓
IF passed → continue
IF failed (3 times) → notify-user: "AI 检测未通过，建议手动优化"
```

---

## 📋 决策树

```
用户指令
  │
  ├─ "发布..." / "发..." → full-publish
  │
  ├─ "生成..." → 
  │   ├─ "...文章" / "...资讯" → generate-only
  │   └─ "...封面" → cover-only
  │
  ├─ "状态" / "检查..." → check-status
  │
  └─ "发布草稿" / "发布已有" → publish-existing
```

---

## 🔁 重试机制

### 通用重试策略

| 操作 | 重试次数 | 间隔 | 降级策略 |
|------|----------|------|----------|
| 文章生成 | 2 | 5 秒 | 通知用户 |
| 封面生成 | 3 | 3 秒 | 切换风格 |
| 浏览器连接 | 3 | 10 秒 | 手动发布 |
| 公众号登录 | 1 | 120 秒 | 等待用户 |
| 发布操作 | 2 | 5 秒 | 保存草稿 |

---

## 📝 日志格式

```
[2026-03-03 14:30:00] [INFO] [ai-publisher-agent] Workflow started: full-publish
[2026-03-03 14:30:01] [INFO] [ai-publisher-agent] Step 2: Checking article status...
[2026-03-03 14:30:02] [INFO] [ai-publisher-agent] Article found: AI-News-2026-03-03.md
[2026-03-03 14:30:03] [INFO] [ai-publisher-agent] Step 3: Checking cover status...
[2026-03-03 14:30:04] [INFO] [ai-publisher-agent] Cover found: cover-2026-03-03.png
[2026-03-03 14:30:05] [INFO] [ai-publisher-agent] Step 4: Checking browser status...
[2026-03-03 14:30:06] [INFO] [ai-publisher-agent] Browser connected: true
[2026-03-03 14:30:10] [INFO] [ai-publisher-agent] Step 5: Checking WeChat login...
[2026-03-03 14:30:15] [INFO] [ai-publisher-agent] WeChat logged in: true
[2026-03-03 14:30:20] [INFO] [ai-publisher-agent] Step 6: Publishing article...
[2026-03-03 14:32:30] [INFO] [ai-publisher-agent] Article published successfully
[2026-03-03 14:32:31] [INFO] [ai-publisher-agent] Workflow completed: full-publish (duration: 151s)
```

---

**版本：** 1.0.0  
**最后更新：** 2026-03-03
