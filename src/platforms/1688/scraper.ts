/**
 * 1688 商品抓取模块
 * 支持商品详情页解析和商品包下载
 */

import { chromium, Browser, Page } from 'playwright';
import { Product, Image } from '../../core/product.js';
import * as cheerio from 'cheerio';
import axios from 'axios';

export interface ScraperOptions {
  headless?: boolean;
  proxy?: string;
  cookie?: string;
  timeout?: number;
}

export class Al1688Scraper {
  private browser: Browser | null = null;
  private options: ScraperOptions;

  constructor(options: ScraperOptions = {}) {
    this.options = {
      headless: true,
      timeout: 30000,
      ...options
    };
  }

  /**
   * 初始化浏览器
   */
  async init(): Promise<void> {
    if (!this.browser) {
      this.browser = await chromium.launch({
        headless: this.options.headless,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage'
        ]
      });
    }
  }

  /**
   * 关闭浏览器
   */
  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }

  /**
   * 抓取商品详情
   */
  async scrapeProduct(url: string): Promise<Product> {
    await this.init();
    
    if (!this.browser) {
      throw new Error('浏览器未初始化');
    }

    const page = await this.browser.newPage({
      viewport: { width: 1920, height: 1080 }
    });

    // 设置 Cookie（如果需要登录）
    if (this.options.cookie) {
      await page.setExtraHTTPHeaders({
        'Cookie': this.options.cookie
      });
    }

    try {
      console.log(`[1688] 开始抓取：${url}`);
      
      // 访问商品页面
      await page.goto(url, { 
        waitUntil: 'networkidle',
        timeout: this.options.timeout 
      });

      // 等待页面加载
      await page.waitForSelector('.d-title, .title', { timeout: 10000 }).catch(() => {
        console.warn('未找到标题元素，尝试继续解析');
      });

      // 获取页面 HTML
      const html = await page.content();
      const $ = cheerio.load(html);

      // 解析商品信息
      const product = await this.parseProduct($, url, page);
      
      console.log(`[1688] 抓取成功：${product.title}`);
      console.log(`[1688] 价格：¥${product.price}, 库存：${product.stock}`);
      console.log(`[1688] SKU 数量：${product.skus.length}`);
      console.log(`[1688] 图片数量：${product.images.length}`);

      return product;
    } finally {
      await page.close();
    }
  }

  /**
   * 解析商品数据
   */
  private async parseProduct($: cheerio.CheerioAPI, url: string, page: Page): Promise<Product> {
    // 标题
    const title = $('.d-title').text().trim() || 
                  $('.title').text().trim() || 
                  $('h1').first().text().trim() || 
                  '未命名商品';

    // 价格（获取价格区间）
    let price = 0;
    const priceText = $('.price-1688, .price, .dt-price').first().text().trim();
    const priceMatch = priceText.match(/¥?\s*([\d.]+)/);
    if (priceMatch) {
      price = parseFloat(priceMatch[1]);
    }

    // 库存
    let stock = 0;
    const stockText = $('.stock, .quantity').first().text().trim();
    const stockMatch = stockText.match(/(\d+)/);
    if (stockMatch) {
      stock = parseInt(stockMatch[1]);
    }

    // 图片
    const images: Image[] = [];
    
    // 主图
    $('.img-container img, .pic-container img, .main-img img').each((i, el) => {
      const src = $(el).attr('data-src') || $(el).attr('src');
      if (src && src.startsWith('http')) {
        images.push({
          url: src,
          type: 'main',
          order: i
        });
      }
    });

    // 详情图（从详情页获取）
    const detailImages = await this.extractDetailImages(page);
    detailImages.forEach((url, i) => {
      images.push({
        url,
        type: 'detail',
        order: images.length + i
      });
    });

    // 描述（详情文本）
    const description = $('.description, .detail, .content').first().text().trim().substring(0, 2000);

    // SKU 信息
    const skus = await this.parseSKUs(page, $);

    // 类目（尝试获取）
    let categoryId = 0;
    const categoryText = $('.category, .breadcrumb').last().text();
    // 类目映射需要后续完善

    // 属性
    const properties: Record<string, string> = {};
    $('.property-item, .attr-item').each((i, el) => {
      const key = $(el).find('.key, .name').first().text().trim();
      const value = $(el).find('.value, .content').first().text().trim();
      if (key && value) {
        properties[key] = value;
      }
    });

    return {
      title,
      description: description || title,
      categoryId,
      price,
      stock,
      skus,
      images,
      properties,
      sourceUrl: url,
      sourcePlatform: '1688'
    };
  }

  /**
   * 解析 SKU
   */
  private async parseSKUs(page: Page, $: cheerio.CheerioAPI) {
    const skus: any[] = [];

    // 尝试从页面脚本中获取 SKU 数据
    const scripts = $('script');
    for (let i = 0; i < scripts.length; i++) {
      const script = $(scripts[i]).html() || '';
      if (script.includes('skuData') || script.includes('sku')) {
        // 尝试提取 SKU JSON 数据
        const jsonMatch = script.match(/\{[^}]*"sku[^}]*\}/);
        if (jsonMatch) {
          try {
            // 这里需要更完善的 JSON 提取逻辑
            console.log('[1688] 找到 SKU 数据');
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }

    // 从页面元素获取 SKU
    $('.sku-item, .option-item').each((i, el) => {
      const properties = $(el).find('.sku-prop').text().trim();
      const priceText = $(el).find('.sku-price').text().trim();
      const stockText = $(el).find('.sku-stock').text().trim();

      const priceMatch = priceText.match(/([\d.]+)/);
      const stockMatch = stockText.match(/(\d+)/);

      if (properties) {
        skus.push({
          properties,
          price: priceMatch ? parseFloat(priceMatch[1]) : 0,
          stock: stockMatch ? parseInt(stockMatch[1]) : 0
        });
      }
    });

    // 如果没有找到 SKU，创建一个默认的
    if (skus.length === 0) {
      skus.push({
        properties: '默认',
        price: 0,
        stock: 0
      });
    }

    return skus;
  }

  /**
   * 提取详情图片
   */
  private async extractDetailImages(page: Page): Promise<string[]> {
    const images: string[] = [];

    // 滚动到页面底部，加载懒加载图片
    await page.evaluate(async () => {
      for (let i = 0; i < 5; i++) {
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    });

    // 获取详情区域的所有图片
    const detailImages = await page.$$eval(
      '.detail-content img, .description img, .content img',
      (imgs: any[]) => imgs.map((img: any) => img.src || img.dataset?.src).filter(Boolean)
    );

    images.push(...detailImages.filter((src: string) => src.startsWith('http')));

    return images;
  }

  /**
   * 批量抓取商品
   */
  async scrapeBatch(urls: string[], concurrency: number = 3): Promise<Product[]> {
    const results: Product[] = [];
    const queue = [...urls];
    const processing = new Set<string>();

    while (queue.length > 0 || processing.size > 0) {
      // 填充并发
      while (processing.size < concurrency && queue.length > 0) {
        const url = queue.shift()!;
        processing.add(url);
        
        this.scrapeProduct(url)
          .then(product => {
            results.push(product);
          })
          .catch(error => {
            console.error(`[1688] 抓取失败：${url}`, error);
          })
          .finally(() => {
            processing.delete(url);
          });
      }

      // 等待一下
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    return results;
  }
}

// 导出单例
export const scraper = new Al1688Scraper();
