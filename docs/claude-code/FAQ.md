# Claude Code 常见问题解答

## 安装问题

### Q: 安装时提示权限错误

**A**: 这是 npm 全局安装的常见问题。

**解决方案**:

```bash
# 方法 1: 使用 sudo (macOS/Linux)
sudo npm install -g @anthropic-ai/claude-code

# 方法 2: 修改 npm 配置 (推荐)
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code

# 方法 3: 使用 nvm
nvm install --lts
npm install -g @anthropic-ai/claude-code
```

### Q: 安装后找不到 claude 命令

**A**: PATH 环境变量未包含 npm 全局包目录。

**解决方案**:

```bash
# 找到安装位置
npm config get prefix

# 添加到 PATH (macOS/Linux)
export PATH=$(npm config get prefix)/bin:$PATH
echo 'export PATH=$(npm config get prefix)/bin:$PATH' >> ~/.bashrc

# Windows PowerShell
$env:Path += ";$(npm config get prefix)\bin"
```

### Q: Node.js 版本不兼容

**A**: Claude Code 需要 Node.js v18 或更高版本。

**解决方案**:

```bash
# 检查当前版本
node --version

# 使用 nvm 升级 (推荐)
nvm install 20
nvm use 20
nvm alias default 20

# 或直接下载新版本
# https://nodejs.org
```

## API 密钥问题

### Q: API 密钥无效或过期

**A**: 可能的原因和解决方案：

1. **密钥复制错误**
   ```bash
   # 确保没有多余空格
   echo $ANTHROPIC_API_KEY | xxd
   ```

2. **账户额度不足**
   - 登录 console.anthropic.com 检查余额
   - 充值或等待下月额度

3. **密钥被撤销**
   - 重新生成新密钥
   - 更新配置

4. **区域限制**
   - 检查 API 端点设置
   - 使用正确的区域配置

### Q: 如何安全存储 API 密钥

**A**: 推荐做法：

```bash
# ✅ 推荐：使用环境变量
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc

# ✅ 推荐：使用配置文件 (限制权限)
echo '{"apiKey": "your-key"}' > ~/.claude/config.json
chmod 600 ~/.claude/config.json

# ❌ 避免：硬编码在代码中
# ❌ 避免：提交到版本控制
```

## 使用问题

### Q: 响应速度慢

**A**: 可能的原因：

1. **网络问题**
   ```bash
   # 测试连接
   ping console.anthropic.com
   
   # 检查延迟
   curl -w "@curl-format.txt" -o /dev/null -s https://console.anthropic.com
   ```

2. **模型负载**
   - 尝试切换到其他模型
   - 避开高峰时段

3. **请求过大**
   - 拆分大任务为小任务
   - 减少上下文大小

### Q: 输出被截断

**A**: 超过最大 token 限制。

**解决方案**:

```
# 请求继续
请继续

# 或要求分部分输出
请分三部分回答，这是第一部分

# 或增加 token 限制
claude --max-tokens 16384
```

### Q: 代码执行失败

**A**: 检查以下几点：

1. **权限问题**
   ```bash
   # 检查文件权限
   ls -la filename
   
   # 修复权限
   chmod +x script.sh
   ```

2. **依赖缺失**
   ```bash
   # 安装依赖
   npm install
   ```

3. **环境差异**
   ```bash
   # 检查 Node 版本
   node --version
   
   # 检查环境变量
   env | grep NODE
   ```

## 文件操作问题

### Q: 无法读取文件

**A**: 检查文件路径和权限。

```bash
# 确认文件存在
ls -la path/to/file

# 检查读取权限
chmod +r path/to/file

# 使用绝对路径
@/absolute/path/to/file
```

### Q: 修改文件后内容丢失

**A**: 可能的原因：

1. **并发修改**
   - 确保没有其他进程修改同一文件
   - 使用版本控制

2. **编码问题**
   ```bash
   # 检查文件编码
   file -I filename
   
   # 统一使用 UTF-8
   iconv -f 原编码 -t UTF-8 file > file.utf8
   ```

3. **写入失败**
   - 检查磁盘空间
   - 检查写入权限

## Git 集成问题

### Q: Git 命令执行失败

**A**: 常见问题：

1. **不在 Git 仓库**
   ```bash
   # 初始化仓库
   git init
   
   # 或进入正确目录
   cd /path/to/repo
   ```

2. **未配置用户信息**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
   ```

3. **有未暂存的更改**
   ```bash
   # 查看状态
   git status
   
   # 暂存更改
   git add .
   ```

### Q: 合并冲突如何解决

**A**: 让 Claude Code 帮助：

```
请帮我解决这个合并冲突：
冲突文件：@src/app.ts

保留两边的更改：
- 保留用户认证的新逻辑
- 保留性能优化的代码
```

## 性能问题

### Q: 内存使用过高

**A**: 优化建议：

1. **减少上下文**
   ```
   只分析关键文件，不要包含整个项目
   ```

2. **分批处理**
   ```
   先处理前 10 个文件，完成后再处理下一批
   ```

3. **定期清理**
   ```bash
   # 清除会话缓存
   rm -rf ~/.claude/cache
   ```

### Q: 响应不准确

**A**: 改进提示词：

```
❌ 模糊：修复这个 bug

✅ 具体：这个函数在输入负数时返回错误结果。
   期望：返回绝对值
   实际：返回原值
   文件：@src/utils/math.ts
   函数：absValue()
```

## 安全问题

### Q: 代码安全吗？

**A**: 注意事项：

1. **不要分享敏感信息**
   - API 密钥
   - 数据库密码
   - 个人隐私数据

2. **审查生成的代码**
   - 检查安全漏洞
   - 验证依赖来源
   - 进行安全测试

3. **遵守公司政策**
   - 确认允许使用 AI 工具
   - 遵循代码审查流程

### Q: 如何防止代码泄露

**A**: 最佳实践：

```bash
# 1. 使用本地模型 (如可用)
claude --local

# 2. 脱敏处理
# 替换敏感信息后再发送

# 3. 私有部署
# 考虑企业版私有部署选项
```

## 高级问题

### Q: 如何自定义模型参数

**A**: 通过配置文件：

```json
{
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 8192,
  "temperature": 0.7,
  "topP": 0.9,
  "timeout": 300000
}
```

### Q: 可以离线使用吗

**A**: 目前需要网络连接访问 API。离线方案：

- 考虑本地部署方案
- 使用缓存减少请求
- 批量处理离线任务

### Q: 如何集成到 CI/CD

**A**: 示例流程：

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      - name: Run Review
        run: claude "Review this PR" --json > review.json
```

## 其他资源

### 获取帮助

- **官方文档**: https://docs.anthropic.com
- **社区论坛**: https://community.anthropic.com
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **技术支持**: support@anthropic.com

### 学习资源

- 官方教程和示例
- 社区最佳实践
- 视频教程
- 案例研究

---

**没找到答案？** 请提供更多细节，Claude Code 可以帮你诊断具体问题。
