# 部署指南

本指南涵盖所有可用的部署方式，包括 GitHub Pages、Docker 容器化部署以及本地开发环境配置。

## 📋 目录

- [本地开发环境](#本地开发环境)
- [GitHub Pages 部署](#github-pages-部署)
- [Docker 容器化部署](#docker-容器化部署)
- [生产部署指南](#生产部署指南)
- [故障排除](#故障排除)

---

## 本地开发环境

### 前置要求

- Node.js >= 20.x
- npm >= 9.x
- Git

### 快速开始

```bash
# 1. 克隆仓库
git clone <repository-url>
cd <project-directory>

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 4. 访问应用
# 打开浏览器访问 http://localhost:3000
```

### 开发命令

```bash
# 启动开发服务器 (热重载)
npm run dev

# 运行测试
npm test

# 代码检查
npm run lint

# 构建生产版本
npm run build
```

### 环境变量配置

创建 `.env` 文件：

```bash
# .env
NODE_ENV=development
PORT=3000
API_URL=http://localhost:3000
```

---

## GitHub Pages 部署

### 自动部署

本项目配置了 GitHub Actions，推送到 `main` 分支时会自动部署到 GitHub Pages。

#### 启用 GitHub Pages

1. 进入仓库 **Settings** > **Pages**
2. Source 选择 **GitHub Actions**
3. 保存配置

#### 手动触发部署

```bash
# 推送更改触发自动部署
git add .
git commit -m "docs: update documentation"
git push origin main

# 或通过 GitHub UI 手动触发
# Actions > Deploy Docs > Run workflow
```

#### 部署工作流说明

- **触发条件**: 
  - 推送到 `main` 分支
  - `docs/` 目录或工作流文件变更
  - 手动触发 (workflow_dispatch)

- **部署流程**:
  1. 检出代码
  2. 配置 Pages 环境
  3. 上传 `docs/` 目录为 artifact
  4. 部署到 GitHub Pages

#### 访问部署站点

部署完成后，访问:
```
https://<username>.github.io/<repository>/
```

---

## Docker 容器化部署

### 前置要求

- Docker >= 24.x
- Docker Compose >= 2.0

### 开发环境部署

```bash
# 启动开发环境
docker compose --profile dev up app-dev

# 后台运行
docker compose --profile dev up -d app-dev

# 查看日志
docker compose logs -f app-dev

# 停止服务
docker compose --profile dev down
```

### 生产环境部署

```bash
# 构建并启动生产环境
docker compose --profile prod up -d

# 查看运行状态
docker compose ps

# 查看应用日志
docker compose logs -f app

# 停止所有服务
docker compose --profile prod down
```

### 单独使用 Docker

```bash
# 构建镜像
docker build -t my-app:latest .

# 运行容器
docker run -d \
  --name my-app \
  -p 3000:3000 \
  -e NODE_ENV=production \
  my-app:latest

# 查看容器日志
docker logs -f my-app

# 停止并删除容器
docker stop my-app && docker rm my-app
```

### Docker 镜像优化

```bash
# 查看镜像大小
docker images my-app

# 清理未使用的镜像
docker image prune -a

# 导出镜像
docker save -o my-app.tar my-app:latest

# 导入镜像
docker load -i my-app.tar
```

---

## 生产部署指南

### 服务器要求

- **CPU**: 2 核心或更高
- **内存**: 2GB RAM 或更高
- **存储**: 10GB 可用空间
- **系统**: Linux (Ubuntu 20.04+ 推荐)

### 生产环境配置

#### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

#### 2. 部署应用

```bash
# 克隆仓库
git clone <repository-url> /opt/my-app
cd /opt/my-app

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置生产环境配置

# 启动服务
docker compose --profile prod up -d

# 设置开机自启
docker compose --profile prod up -d
```

#### 3. 配置 Nginx (可选)

创建 `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:3000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

#### 4. SSL 配置 (推荐)

使用 Let's Encrypt:

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

### 监控与日志

```bash
# 查看服务状态
docker compose ps

# 实时日志
docker compose logs -f app

# 资源使用
docker stats

# 进入容器
docker compose exec app sh
```

### 备份策略

```bash
# 备份数据卷
docker run --rm \
  -v app_app-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz -C /data .

# 恢复数据
docker run --rm \
  -v app_app-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /data
```

### 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重新构建并部署
docker compose --profile prod up -d --build

# 清理旧镜像
docker image prune -f
```

---

## 故障排除

### 常见问题

#### GitHub Pages 部署失败

```bash
# 检查 Actions 权限
# Settings > Actions > General > Workflow permissions
# 确保 "Read and write permissions" 已启用

# 手动重新运行工作流
# Actions > Deploy Docs > 选择失败的运行 > Re-run jobs
```

#### Docker 容器无法启动

```bash
# 查看容器日志
docker compose logs app

# 检查端口占用
sudo lsof -i :3000

# 重建容器
docker compose --profile prod up -d --force-recreate
```

#### 内存不足

```bash
# 限制容器内存
# 在 docker-compose.yml 中添加:
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
```

#### 网络问题

```bash
# 重启 Docker 网络
docker network prune

# 重建网络
docker compose down
docker compose up -d
```

### 获取帮助

- 查看日志：`docker compose logs -f`
- 健康检查：`docker compose ps`
- 资源监控：`docker stats`

---

## 安全建议

1. **定期更新**: 保持基础镜像和依赖最新
2. **最小权限**: 使用非 root 用户运行容器
3. **环境变量**: 敏感信息使用环境变量，不要硬编码
4. **网络隔离**: 生产环境使用独立网络
5. **日志审计**: 定期审查应用和安全日志

---

**最后更新**: 2026-03-15
