# 5 分钟快速开始 ⚡

## 前提条件

- ✅ 有淘宝店铺
- ✅ Node.js 18+ 已安装
- ✅ 能访问 1688 和淘宝

---

## 步骤 1：安装依赖（1 分钟）

```bash
npm install
```

---

## 步骤 2：获取淘宝 API 凭证（2 分钟）

**最快方法**：

1. 访问 https://api.taobao.com/api/api.htm
2. 登录你的淘宝店铺账号
3. 搜索 `taobao.item.add`
4. 点击「授权」，同意授权
5. 页面会显示你的 API 凭证
6. 复制 `app_key`、`app_secret`、`access_token`

---

## 步骤 3：配置（30 秒）

创建 `.env` 文件：

```bash
TAOBAO_APP_KEY=刚才复制的 app_key
TAOBAO_APP_SECRET=刚才复制的 app_secret
TAOBAO_ACCESS_TOKEN=刚才复制的 access_token
```

---

## 步骤 4：测试（1 分钟）

找个 1688 商品，复制链接，运行：

```bash
npm run dev -- https://detail.1688.com/offer/xxxxxxxxx.html
```

等待发布完成，去淘宝店铺后台查看！

---

## 完成！🎉

现在你可以：

- ✅ 批量发布 1688 商品到淘宝
- ✅ 自动处理图片
- ✅ 自动映射类目和属性
- ✅ 自动加价（默认 20% 利润率）

---

## 下一步

详细文档：
- 📖 [完整使用说明](USAGE.md)
- 📖 [项目架构](README.md)
- 🔧 [故障排查](USAGE.md#常见问题排查)

---

**有问题？直接问小助手！** 🤖
