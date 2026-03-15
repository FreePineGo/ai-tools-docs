# 使用指南 📖

## 第一步：获取淘宝 API 凭证

### 1. 注册淘宝开放平台

1. 访问 https://open.taobao.com
2. 用你的淘宝店铺账号登录
3. 完成开发者认证（需要店铺资质）

### 2. 创建应用

1. 进入「应用管理」→「创建应用」
2. 选择「自研应用」
3. 填写应用信息：
   - 应用名称：AI Publisher（或任意名称）
   - 应用描述：商品自动发布工具
   - 回调 URL：可以填 `http://localhost:3000`（本地测试用）

### 3. 申请 API 权限

在应用管理页面，申请以下 API 权限：

```
taobao.item.add          - 发布商品
taobao.item.update       - 更新商品
taobao.item.delete       - 删除商品
taobao.item.get          - 获取商品信息
taobao.itemcats.get      - 获取商品类目
taobao.itemprops.get     - 获取商品属性
taobao.picture.upload    - 上传图片到图片空间
taobao.items.list        - 获取店铺商品列表
```

**注意**：部分 API 需要店铺达到一定等级才能申请。

### 4. 获取 Access Token

#### 方法 1：使用沙箱环境测试

1. 访问 https://console.open.taobao.com/sandbox
2. 使用沙箱账号测试 API
3. 获取沙箱 Token

#### 方法 2：正式环境（推荐）

使用淘宝提供的授权工具获取：

1. 访问 https://oauth.taobao.com/authorize
2. 构造授权 URL：
   ```
   https://oauth.taobao.com/authorize?
     response_type=code&
     client_id=YOUR_APP_KEY&
     redirect_uri=YOUR_REDIRECT_URL&
     state=12345&
     view=web
   ```
3. 用店铺账号授权
4. 获取授权码（code）
5. 用授权码换取 Access Token

#### 方法 3：使用工具快速获取（最简单）

使用淘宝 API 调试工具：
https://api.taobao.com/api/api.htm

1. 选择任意 API（如 `taobao.item.get`）
2. 点击「授权」
3. 登录后会自动获取 Token
4. 复制 Token 到 `.env` 文件

---

## 第二步：配置项目

### 1. 复制环境变量文件

```bash
cp .env.example .env
```

### 2. 填写配置

编辑 `.env` 文件：

```bash
# 淘宝 API 配置
TAOBAO_APP_KEY=你的 app_key
TAOBAO_APP_SECRET=你的 app_secret
TAOBAO_ACCESS_TOKEN=你的 access_token

# 1688 Cookie（可选，如果抓取失败再配置）
# 登录 1688.com 后，在浏览器控制台运行：
# console.log(document.cookie)
# 复制输出内容到这里
ALIBABA_COOKIE=

# 代理（可选，如果 1688 反爬严重）
PROXY_URL=http://127.0.0.1:7890
```

---

## 第三步：测试运行

### 测试 1：单个商品发布

```bash
npm run dev -- https://detail.1688.com/offer/123456789.html
```

### 测试 2：批量发布

```bash
npm run dev -- \
  https://detail.1688.com/offer/1.html \
  https://detail.1688.com/offer/2.html \
  https://detail.1688.com/offer/3.html
```

### 测试 3：沙箱环境测试

在 `src/index.ts` 中修改：

```typescript
taobao: {
  appKey: '沙箱 app_key',
  appSecret: '沙箱 app_secret',
  accessToken: '沙箱 token',
  sandbox: true,  // 开启沙箱模式
  profitMargin: 0.2
}
```

---

## 第四步：日常使用

### 场景 1：看到 1688 好货，想上架到淘宝

1. 复制 1688 商品链接
2. 运行命令：
   ```bash
   npm run dev -- <商品链接>
   ```
3. 等待发布完成
4. 到淘宝店铺后台查看商品

### 场景 2：批量上架（比如 10 个商品）

1. 收集 10 个 1688 商品链接
2. 运行命令：
   ```bash
   npm run dev -- 链接 1 链接 2 链接 3 ... 链接 10
   ```
3. 工具会自动并发处理（默认 3 个并发）
4. 查看发布结果统计

### 场景 3：定期更新库存/价格

后续会支持从 1688 同步库存和价格到淘宝：

```bash
npm run sync -- --stock  # 同步库存
npm run sync -- --price  # 同步价格
```

---

## 常见问题排查

### ❌ 抓取 1688 失败

**现象**：提示「抓取失败」或「页面不存在」

**原因**：1688 有反爬机制

**解决方案**：
1. 在浏览器登录 1688
2. 按 F12 打开控制台
3. 运行 `console.log(document.cookie)`
4. 复制输出到 `.env` 的 `ALIBABA_COOKIE`
5. 重试

如果还不行，配置代理：
```bash
PROXY_URL=http://你的代理 IP:端口
```

### ❌ 淘宝发布失败 - 类目错误

**现象**：提示「类目选择错误」或「缺少必填属性」

**原因**：1688 类目和淘宝类目映射不准确

**解决方案**：
1. 手动确认商品应该属于哪个淘宝类目
2. 在 `src/platforms/taobao/mapper.ts` 中添加映射：
   ```typescript
   '你的类目名': 淘宝类目 ID
   ```
3. 或者在发布时手动指定类目

### ❌ 淘宝发布失败 - Token 过期

**现象**：提示「授权已过期」或「Invalid Token」

**原因**：Access Token 有有效期

**解决方案**：
1. 重新获取 Token（参考第一步）
2. 更新 `.env` 文件
3. 重试

### ❌ 图片上传失败

**现象**：商品发布成功，但图片缺失

**原因**：图片空间上传失败

**解决方案**：
1. 检查图片链接是否可访问
2. 手动上传图片到淘宝图片空间
3. 在发布后手动关联图片

---

## 高级用法

### 自定义利润率

在 `src/index.ts` 中修改：

```typescript
taobao: {
  profitMargin: 0.3  // 30% 利润率
}
```

或者根据商品类目设置不同利润率：

```typescript
// TODO: 后续支持
const profitMargins = {
  '服装': 0.4,
  '数码': 0.15,
  '家居': 0.25
};
```

### 并发控制

默认并发 3 个商品，可以调整：

```typescript
const queue = new PublishQueue(5);  // 并发 5 个
```

**注意**：并发太高可能触发淘宝 API 限流。

### 失败重试

默认失败重试 3 次，可以调整：

```typescript
queue.add(product, 5);  // 最多重试 5 次
```

---

## 下一步

1. **完善类目映射** - 根据你的商品类目，完善 `mapper.ts`
2. **配置自动同步** - 设置定时任务，定期同步 1688 库存/价格
3. **扩展其他平台** - 参考淘宝模块，实现拼多多、抖音适配

---

**有问题？随时问小助手** 🤖
