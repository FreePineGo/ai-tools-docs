/**
 * AI Publisher Agent - 主入口
 * 1688 商品一键发布到淘宝
 */

import dotenv from 'dotenv';
import { Al1688Scraper } from './platforms/1688/scraper.js';
import { Al1688Downloader } from './platforms/1688/downloader.js';
import { TaobaoPublisher } from './platforms/taobao/publisher.js';
import { PublishQueue } from './core/queue.js';
import { Product } from './core/product.js';

// 加载环境变量
dotenv.config();

// 配置
const CONFIG = {
  taobao: {
    appKey: process.env.TAOBAO_APP_KEY || '',
    appSecret: process.env.TAOBAO_APP_SECRET || '',
    accessToken: process.env.TAOBAO_ACCESS_TOKEN || '',
    sandbox: false,
    profitMargin: 0.2  // 20% 利润率
  },
  al1688: {
    cookie: process.env.ALIBABA_COOKIE || '',
    proxy: process.env.PROXY_URL
  },
  image: {
    downloadDir: './temp/images',
    processImages: true
  }
};

/**
 * 主函数：从 1688 抓取并发布到淘宝
 */
async function publishFrom1688(productUrls: string[]): Promise<void> {
  console.log('🚀 AI Publisher Agent 启动');
  console.log(`📦 待处理商品数量：${productUrls.length}`);

  // 检查配置
  if (!CONFIG.taobao.appKey || !CONFIG.taobao.appSecret || !CONFIG.taobao.accessToken) {
    console.error('❌ 请配置淘宝 API 凭证（TAOBAO_APP_KEY, TAOBAO_APP_SECRET, TAOBAO_ACCESS_TOKEN）');
    console.error('📖 参考：https://open.taobao.com');
    return;
  }

  // 初始化组件
  const scraper = new Al1688Scraper({
    cookie: CONFIG.al1688.cookie,
    proxy: CONFIG.al1688.proxy,
    headless: true
  });

  const downloader = new Al1688Downloader({
    outputDir: './temp/packages',
    downloadImages: CONFIG.image.downloadDir !== undefined,
    processImages: CONFIG.image.processImages
  });

  const publisher = new TaobaoPublisher({
    ...CONFIG.taobao,
    imageDir: CONFIG.image.downloadDir
  });

  const queue = new PublishQueue(3);  // 并发 3 个

  try {
    // 1. 抓取商品
    console.log('\n📥 步骤 1: 从 1688 抓取商品...');
    const products: Product[] = [];

    for (const url of productUrls) {
      try {
        console.log(`  抓取：${url}`);
        const product = await scraper.scrapeProduct(url);
        products.push(product);
        console.log(`  ✓ ${product.title.substring(0, 30)}...`);
      } catch (error: any) {
        console.error(`  ✗ 抓取失败：${url} - ${error.message}`);
      }
    }

    if (products.length === 0) {
      console.error('❌ 没有成功抓取到任何商品');
      return;
    }

    console.log(`✓ 成功抓取 ${products.length} 个商品\n`);

    // 2. 添加到发布队列
    console.log('📋 步骤 2: 添加到发布队列...');
    products.forEach(product => queue.add(product));

    // 3. 发布到淘宝
    console.log('📤 步骤 3: 发布到淘宝...\n');
    
    await queue.process(async (product) => {
      return await publisher.publish(product);
    });

    // 4. 输出结果
    console.log('\n📊 发布结果统计:');
    const stats = queue.getStats();
    console.log(`  总计：${stats.total}`);
    console.log(`  ✅ 成功：${stats.success}`);
    console.log(`  ❌ 失败：${stats.failed}`);

    // 显示失败详情
    const failedItems = queue.getAll().filter(item => item.status === 'failed');
    if (failedItems.length > 0) {
      console.log('\n⚠️  失败商品:');
      failedItems.forEach(item => {
        console.log(`  - ${item.product.title.substring(0, 30)}... : ${item.error}`);
      });
    }

  } catch (error: any) {
    console.error('❌ 程序执行失败:', error);
  } finally {
    // 清理资源
    await scraper.close();
    console.log('\n👋 程序结束');
  }
}

/**
 * 从商品包发布
 */
async function publishFromPackage(packagePath: string): Promise<void> {
  console.log('🚀 从商品包发布');
  console.log(`📦 商品包路径：${packagePath}`);

  // TODO: 实现商品包解析逻辑
  console.log('⚠️  商品包解析功能开发中...');
}

/**
 * CLI 入口
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
🤖 AI Publisher Agent - 1688 商品一键发布工具

用法:
  npm run dev -- <1688 商品链接 1> [链接 2] [链接 3] ...
  npm run dev -- --package <商品包路径>

示例:
  npm run dev -- https://detail.1688.com/offer/123456.html
  npm run dev -- --package ./downloads/product.csv

配置:
  复制 .env.example 为 .env，填写淘宝 API 凭证
`);
    return;
  }

  // 检查是否是商品包模式
  if (args[0] === '--package') {
    await publishFromPackage(args[1]);
  } else {
    // 商品链接模式
    await publishFrom1688(args);
  }
}

// 运行
main().catch(console.error);
