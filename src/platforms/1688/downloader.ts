/**
 * 1688 商品包下载模块
 * 支持下载淘宝助理数据包格式
 */

import axios from 'axios';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';
import { mkdir, readdir } from 'fs/promises';
import { join } from 'path';
import { downloadAndProcess } from '../../core/image.js';

export interface DownloadOptions {
  outputDir: string;
  downloadImages?: boolean;
  processImages?: boolean;
}

export class Al1688Downloader {
  private options: DownloadOptions;

  constructor(options: DownloadOptions) {
    this.options = {
      downloadImages: true,
      processImages: true,
      ...options
    };
  }

  /**
   * 下载商品包
   * 1688 商品包通常是 CSV + 图片的格式
   */
  async downloadProductPackage(productUrl: string): Promise<string> {
    const outputDir = this.options.outputDir;
    
    // 创建输出目录
    await mkdir(outputDir, { recursive: true });

    console.log(`[1688] 开始下载商品包：${productUrl}`);

    // 1688 商品包下载通常需要登录和特定 API
    // 这里提供两种方案：
    // 1. 使用 1688 官方的"下载商品"功能（需要登录）
    // 2. 手动解析页面获取数据

    try {
      // 方案 1: 尝试直接下载（如果 URL 是数据包链接）
      if (productUrl.includes('offer') || productUrl.includes('product')) {
        // 提取商品 ID
        const productId = this.extractProductId(productUrl);
        if (productId) {
          return await this.downloadById(productId);
        }
      }

      // 方案 2: 使用 scraper 抓取后生成数据包
      console.log('[1688] 使用抓取方式生成数据包');
      const { scraper } = await import('./scraper.js');
      const product = await scraper.scrapeProduct(productUrl);
      
      // 生成 CSV 数据包
      const csvPath = await this.generateCSV(product, outputDir);
      
      // 下载图片
      if (this.options.downloadImages) {
        await this.downloadImages(product, join(outputDir, 'images'));
      }

      console.log(`[1688] 商品包下载完成：${csvPath}`);
      return csvPath;
    } catch (error) {
      console.error('[1688] 商品包下载失败:', error);
      throw error;
    }
  }

  /**
   * 通过商品 ID 下载
   */
  private async downloadById(productId: string): Promise<string> {
    // 1688 商品包下载 API（需要登录态）
    // 这里提供一个示例结构，实际使用需要配置 Cookie
    
    const downloadUrl = `https://detail.1688.com/offer/${productId}.html`;
    
    // 实际下载逻辑需要根据 1688 的具体接口调整
    console.log(`[1688] 商品 ID: ${productId}`);
    
    return this.downloadProductPackage(downloadUrl);
  }

  /**
   * 提取商品 ID
   */
  private extractProductId(url: string): string | null {
    const patterns = [
      /offer\/(\d+)\.html/,
      /product\/(\d+)\.html/,
      /id=(\d+)/
    ];

    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) {
        return match[1];
      }
    }

    return null;
  }

  /**
   * 生成 CSV 数据包（淘宝助理格式）
   */
  private async generateCSV(product: any, outputDir: string): Promise<string> {
    const csvPath = join(outputDir, 'product.csv');
    
    // 淘宝助理 CSV 格式示例
    const headers = [
      '商品 ID', '商品标题', '商品描述', '类目 ID', '价格', 
      '库存', 'SKU', '图片', '属性', '来源链接'
    ];

    const row = [
      '',  // 商品 ID（发布后才有）
      product.title,
      product.description,
      product.categoryId,
      product.price,
      product.stock,
      JSON.stringify(product.skus),
      JSON.stringify(product.images.map((img: any) => img.url)),
      JSON.stringify(product.properties),
      product.sourceUrl
    ];

    const csvContent = [
      headers.join(','),
      row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
    ].join('\n');

    await pipeline(
      this.stringToStream(csvContent),
      createWriteStream(csvPath)
    );

    return csvPath;
  }

  /**
   * 下载商品图片
   */
  private async downloadImages(product: any, imageDir: string): Promise<void> {
    await mkdir(imageDir, { recursive: true });

    const images = product.images || [];
    console.log(`[1688] 开始下载 ${images.length} 张图片...`);

    for (let i = 0; i < images.length; i++) {
      const image = images[i];
      const ext = image.url.split('.').pop()?.split('?')[0] || 'jpg';
      const filename = `${image.type}_${i}.${ext}`;
      const outputPath = join(imageDir, filename);

      try {
        if (this.options.processImages) {
          await downloadAndProcess(image.url, outputPath);
        } else {
          const response = await axios({
            url: image.url,
            method: 'GET',
            responseType: 'stream'
          });
          await pipeline(response.data, createWriteStream(outputPath));
        }
        
        // 更新图片路径为本地路径
        image.localPath = outputPath;
        
        console.log(`[1688] 图片 ${i + 1}/${images.length} 下载完成`);
      } catch (error) {
        console.error(`[1688] 图片下载失败：${image.url}`, error);
      }
    }
  }

  /**
   * 字符串流转为流
   */
  private stringToStream(str: string): any {
    const { Readable } = require('stream');
    return Readable.from(str);
  }

  /**
   * 批量下载商品包
   */
  async downloadBatch(urls: string[], outputBaseDir: string): Promise<string[]> {
    const results: string[] = [];

    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      const outputDir = join(outputBaseDir, `product_${i + 1}`);
      
      console.log(`[1688] 下载 ${i + 1}/${urls.length}: ${url}`);
      
      try {
        const result = await this.downloadProductPackage(url);
        results.push(result);
      } catch (error) {
        console.error(`[1688] 下载失败：${url}`, error);
      }
    }

    return results;
  }
}
