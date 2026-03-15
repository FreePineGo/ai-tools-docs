# 小红书每日文案生成任务

## 任务说明

这是一个可重复执行的任务，用于生成当天的小红书文案。

## 执行方式

### 方式 1：手动触发
和 AI 助手说：
```
执行小红书每日任务
```

### 方式 2：定时任务调用
使用 Windows 任务计划程序 + PowerShell 脚本调用

## PowerShell 调用脚本

创建文件：`D:\自动化任务\小红书\trigger_agent.ps1`

```powershell
# 小红书 AI Agent 触发脚本
# 通过 OpenClaw sessions_spawn 调用

$task = "生成今天的小红书文案，保存到 D:\自动化任务\小红书\输出\"

# 方法 1：如果 OpenClaw 有 CLI
# openclaw sessions spawn --task "$task" --label "xiaohongshu-daily"

# 方法 2：通过 HTTP API（如果支持）
# $response = Invoke-RestMethod -Uri "http://localhost:PORT/sessions/spawn" -Method POST -Body @{
#     task = $task
#     label = "xiaohongshu-daily"
#     mode = "run"
# } | ConvertTo-Json

# 方法 3：通过消息队列或文件触发
# 创建触发文件
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$triggerFile = "D:\自动化任务\小红书\.trigger"
$content = @"
触发时间：$date
任务：生成今天的小红书文案
类型：自动触发
"@
$content | Out-File -FilePath $triggerFile -Encoding UTF8

Write-Host "触发文件已创建：$triggerFile"
Write-Host "AI 助手检测到文件后会自动执行任务"
```

## 文件触发机制

### 原理
1. 定时任务创建触发文件
2. AI 助手定期检测触发文件
3. 检测到后执行任务
4. 执行完成后删除触发文件

### 触发文件格式
```
触发时间：2026-03-05 09:00:00
任务：生成今天的小红书文案
类型：自动触发
```

### AI 助手检测逻辑
```
如果检测到 D:\自动化任务\小红书\.trigger 文件：
    1. 读取文件内容
    2. 执行指定任务
    3. 生成文案
    4. 保存到输出文件夹
    5. 删除触发文件
    6. 通知用户
```

## 输出说明

生成完成后：
- 文件位置：`D:\自动化任务\小红书\输出\日文案_主题_日期.md`
- 包含：标题、正文、标签、AI 配图提示词、发布 checklist

## 错误处理

如果执行失败：
1. 记录错误到日志文件
2. 保留触发文件（不删除）
3. 下次检测时重试
