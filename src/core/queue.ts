/**
 * 发布队列管理
 * 支持失败重试、状态追踪
 */

import { Product, PublishResult } from './product.js';

export type QueueStatus = 'pending' | 'processing' | 'success' | 'failed';

export interface QueueItem {
  id: string;
  product: Product;
  status: QueueStatus;
  retryCount: number;
  maxRetries: number;
  result?: PublishResult;
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface QueueStats {
  total: number;
  pending: number;
  processing: number;
  success: number;
  failed: number;
}

export class PublishQueue {
  private items: Map<string, QueueItem> = new Map();
  private processing: Set<string> = new Set();
  private maxConcurrent: number;

  constructor(maxConcurrent: number = 3) {
    this.maxConcurrent = maxConcurrent;
  }

  /**
   * 添加商品到队列
   */
  add(product: Product, maxRetries: number = 3): string {
    const id = this.generateId(product);
    
    const item: QueueItem = {
      id,
      product,
      status: 'pending',
      retryCount: 0,
      maxRetries,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    this.items.set(id, item);
    console.log(`[队列] 添加商品：${product.title.substring(0, 20)}... (ID: ${id})`);
    
    return id;
  }

  /**
   * 获取下一个待处理的商品
   */
  async getNext(): Promise<QueueItem | null> {
    if (this.processing.size >= this.maxConcurrent) {
      return null;
    }

    for (const item of this.items.values()) {
      if (item.status === 'pending' && !this.processing.has(item.id)) {
        item.status = 'processing';
        item.updatedAt = new Date();
        this.processing.add(item.id);
        return item;
      }
    }

    return null;
  }

  /**
   * 标记为成功
   */
  markSuccess(id: string, result: PublishResult): void {
    const item = this.items.get(id);
    if (item) {
      item.status = 'success';
      item.result = result;
      item.updatedAt = new Date();
      this.processing.delete(id);
      console.log(`[队列] 发布成功：${id}`);
    }
  }

  /**
   * 标记为失败（支持重试）
   */
  markFailed(id: string, error: string): void {
    const item = this.items.get(id);
    if (item) {
      item.retryCount++;
      item.error = error;
      item.updatedAt = new Date();
      this.processing.delete(id);

      if (item.retryCount < item.maxRetries) {
        item.status = 'pending';
        console.log(`[队列] 发布失败，将重试 (${item.retryCount}/${item.maxRetries})：${id}`);
      } else {
        item.status = 'failed';
        console.log(`[队列] 发布失败，已达最大重试次数：${id}`);
      }
    }
  }

  /**
   * 获取队列统计
   */
  getStats(): QueueStats {
    const stats: QueueStats = {
      total: this.items.size,
      pending: 0,
      processing: 0,
      success: 0,
      failed: 0
    };

    for (const item of this.items.values()) {
      stats[item.status]++;
    }

    return stats;
  }

  /**
   * 获取所有商品
   */
  getAll(): QueueItem[] {
    return Array.from(this.items.values());
  }

  /**
   * 生成唯一 ID
   */
  private generateId(product: Product): string {
    const source = product.sourceUrl || 'manual';
    const hash = Buffer.from(source).toString('base64').substring(0, 8);
    return `prod_${hash}_${Date.now()}`;
  }

  /**
   * 处理队列（自动消费）
   */
  async process(
    publisher: (product: Product) => Promise<PublishResult>
  ): Promise<void> {
    const processItem = async (item: QueueItem) => {
      try {
        const result = await publisher(item.product);
        if (result.success) {
          this.markSuccess(item.id, result);
        } else {
          this.markFailed(item.id, result.error || '未知错误');
        }
      } catch (error) {
        this.markFailed(item.id, error instanceof Error ? error.message : String(error));
      }
    };

    // 持续处理直到队列为空
    while (true) {
      const item = await this.getNext();
      if (!item) {
        // 检查是否还有正在处理的
        if (this.processing.size === 0) {
          break;
        }
        // 等待一下再检查
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }

      // 并发处理
      processItem(item).catch(console.error);
    }

    console.log('[队列] 所有商品处理完成');
  }
}
