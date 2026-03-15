/**
 * 淘宝商品发布模块
 */

import { TaobaoAPI } from './api.js';
import { mapper } from './mapper.js';
import { Product, PublishResult } from '../../core/product.js';
import { downloadAndProcess } from '../../core/image.js';
import { mkdir } from 'fs/promises';
import { join } from 'path';

export interface PublisherConfig {
  appKey: string;
  appSecret: string;
  accessToken: string;
  sandbox?: boolean;
  profitMargin?: number;  // 利润率
  autoUploadImages?: boolean;
  imageDir?: string;
}

export class TaobaoPublisher {
  private api: TaobaoAPI;
  private config: PublisherConfig;

  constructor(config: PublisherConfig) {
    this.config = {
      profitMargin: 0.2,
      autoUploadImages: true,
      ...config
    };
    
    this.api = new TaobaoAPI({
      appKey: config.appKey,
      appSecret: config.appSecret,
      accessToken: config.accessToken,
      sandbox: config.sandbox
    });
  }

  /**
   * 发布单个商品
   */
  async publish(product: Product): Promise<PublishResult> {
    try {
      console.log(`[淘宝] 开始发布商品：${product.title.substring(0, 30)}...`);

      // 1. 下载并处理图片
      let processedProduct = product;
      if (this.config.autoUploadImages && product.images?.length > 0) {
        processedProduct = await this.processImages(product);
      }

      // 2. 转换商品格式
      const taobaoItem = await mapper.convertToTaobaoFormat(
        processedProduct, 
        this.api
      );

      // 3. 应用利润率
      if (this.config.profitMargin) {
        taobaoItem.price = Math.round(
          taobaoItem.price * (1 + this.config.profitMargin) * 100
        ) / 100;
        
        if (taobaoItem.skus) {
          taobaoItem.skus.forEach((sku: any) => {
            sku.price = Math.round(sku.price * (1 + this.config.profitMargin) * 100) / 100;
          });
        }
      }

      // 4. 发布商品
      const itemId = await this.api.addItem(taobaoItem);

      console.log(`[淘宝] 发布成功，商品 ID: ${itemId}`);

      return {
        success: true,
        itemId,
        warnings: []
      };
    } catch (error: any) {
      console.error('[淘宝] 发布失败:', error);
      
      return {
        success: false,
        error: error.message || '发布失败'
      };
    }
  }

  /**
   * 处理商品图片
   */
  private async processImages(product: Product): Promise<Product> {
    const imageDir = this.config.imageDir || './temp/images';
    await mkdir(imageDir, { recursive: true });

    const processedImages = [...product.images];

    console.log(`[淘宝] 处理 ${processedImages.length} 张图片...`);

    for (let i = 0; i < processedImages.length; i++) {
      const image = processedImages[i];
      const ext = image.url.split('.').pop()?.split('?')[0] || 'jpg';
      const filename = `${image.type}_${i}_${Date.now()}.${ext}`;
      const outputPath = join(imageDir, filename);

      try {
        // 下载并处理图片
        await downloadAndProcess(image.url, outputPath, {
          maxWidth: 800,
          maxHeight: 800,
          quality: 85,
          format: 'jpeg'
        });

        // 上传到淘宝图片空间
        // const imageUrl = await this.api.uploadImage(outputPath);
        // image.url = imageUrl;
        
        // 暂时使用本地路径，实际使用需要上传
        console.log(`[淘宝] 图片 ${i + 1}/${processedImages.length} 处理完成`);
      } catch (error) {
        console.error(`[淘宝] 图片处理失败：${image.url}`, error);
      }
    }

    return {
      ...product,
      images: processedImages
    };
  }

  /**
   * 批量发布商品
   */
  async publishBatch(products: Product[], concurrency: number = 3): Promise<PublishResult[]> {
    const results: PublishResult[] = [];
    const queue = [...products];
    const processing = new Set<number>();

    console.log(`[淘宝] 开始批量发布 ${products.length} 个商品`);

    while (queue.length > 0 || processing.size > 0) {
      // 填充并发
      while (processing.size < concurrency && queue.length > 0) {
        const index = products.length - queue.length;
        const product = queue.shift()!;
        processing.add(index);

        this.publish(product)
          .then(result => {
            results[index] = result;
          })
          .catch(error => {
            results[index] = {
              success: false,
              error: error.message
            };
          })
          .finally(() => {
            processing.delete(index);
          });
      }

      // 等待一下
      if (processing.size > 0) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    // 统计结果
    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;

    console.log(`[淘宝] 批量发布完成：成功 ${successCount}, 失败 ${failCount}`);

    return results;
  }

  /**
   * 更新商品
   */
  async update(itemId: string, updates: Partial<Product>): Promise<boolean> {
    try {
      // 获取原商品信息
      const item = await this.api.getItem(itemId);
      
      // 合并更新
      const updatedItem = {
        ...item,
        ...updates
      };

      // 调用更新 API
      const result = await this.api.updateItem(itemId, updatedItem);
      
      console.log(`[淘宝] 商品更新成功：${itemId}`);
      
      return result;
    } catch (error: any) {
      console.error('[淘宝] 商品更新失败:', error);
      return false;
    }
  }

  /**
   * 删除商品
   */
  async delete(itemId: string): Promise<boolean> {
    try {
      const result = await this.api.deleteItem(itemId);
      console.log(`[淘宝] 商品删除成功：${itemId}`);
      return result;
    } catch (error: any) {
      console.error('[淘宝] 商品删除失败:', error);
      return false;
    }
  }

  /**
   * 同步库存
   */
  async syncStock(itemId: string, stock: number): Promise<boolean> {
    return this.update(itemId, { stock });
  }

  /**
   * 同步价格
   */
  async syncPrice(itemId: string, price: number): Promise<boolean> {
    return this.update(itemId, { price });
  }
}
