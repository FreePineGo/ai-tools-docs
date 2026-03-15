# 🚀 部署到 GitHub Pages 指南

---

## 📋 快速部署步骤

### 步骤 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`ai-tools-docs`
3. 描述：`AI 工具使用文档 - OpenClaw, Claude Code, Codex 等完整指南`
4. 选择 **Public**
5. **不要** 初始化 README
6. 点击 **Create repository**

---

### 步骤 2: 推送代码

```bash
# 进入项目目录
cd C:\Users\1\.openclaw\workspace\agents\ai-publisher-agent

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "docs: 初始版本 - AI 工具完整文档"

# 添加远程仓库 (替换 YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-tools-docs.git

# 推送
git push -u origin main
```

---

### 步骤 3: 配置 GitHub Pages

1. 访问你的 GitHub 仓库
2. 进入 **Settings** -> **Pages**
3. **Source** 选择 `Deploy from a branch`
4. **Branch** 选择 `main`
5. **Folder** 选择 `/docs`
6. 点击 **Save**

---

### 步骤 4: 等待部署

- GitHub 会在 2-5 分钟内构建
- 完成后访问：`https://YOUR_USERNAME.github.io/ai-tools-docs/`

---

## 🐳 Docker 部署 (可选)

### 本地开发

```bash
docker compose --profile dev up
```

访问：http://localhost:8080

### 生产部署

```bash
docker compose up -d
```

访问：http://localhost:80

---

## 📊 项目结构

```
ai-publisher-agent/
├── docs/                       # 文档目录 (部署到 GitHub Pages)
│   ├── README.md               # 总索引
│   ├── INDEX.md                # 完整索引
│   ├── openclaw/               # OpenClaw 文档
│   ├── claude-code/            # Claude Code 文档
│   ├── codex/                  # Codex 文档
│   ├── cursor/                 # Cursor 文档
│   ├── copilot/                # Copilot 文档
│   ├── windsurf/               # Windsurf 文档
│   ├── aider/                  # Aider 文档
│   └── guides/                 # 使用指南
│
├── Dockerfile                  # Docker 配置
├── docker-compose.yml          # Docker Compose
└── .github/workflows/
    └── deploy-docs.yml         # GitHub Actions
```

---

## ✅ 部署检查清单

- [ ] GitHub 仓库已创建
- [ ] 代码已推送
- [ ] GitHub Pages 已配置
- [ ] 文档可正常访问
- [ ] 所有链接有效
- [ ] 移动端适配正常

---

## 🔗 相关链接

- GitHub Pages: https://docs.github.com/en/pages
- 示例部署：https://username.github.io/ai-tools-docs/

---

*部署完成后，每次推送到 main 分支都会自动更新文档！* 🚀
