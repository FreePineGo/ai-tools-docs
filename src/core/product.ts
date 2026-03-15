/**
 * 商品数据模型
 * 统一 1688 和淘宝的商品结构
 */

export interface SKU {
  properties: string;        // SKU 属性，如 "颜色：红色;尺码:L"
  price: number;             // 价格
  stock: number;             // 库存
  skuId?: string;            // SKU ID
}

export interface Image {
  url: string;               // 图片 URL
  type: 'main' | 'detail' | 'sku';  // 图片类型
  order?: number;            // 排序
}

export interface Product {
  // 基本信息
  title: string;             // 标题
  description: string;       // 描述
  categoryId: number;        // 类目 ID
  
  // 价格库存
  price: number;             // 价格
  originalPrice?: number;    // 原价
  stock: number;             // 总库存
  
  // SKU
  skus: SKU[];               // SKU 列表
  
  // 图片
  images: Image[];           // 图片列表
  
  // 属性
  properties: Record<string, string>;  // 商品属性
  
  // 来源
  sourceUrl?: string;        // 来源链接（1688 商品链接）
  sourcePlatform?: '1688' | 'taobao' | 'pinduoduo' | 'douyin';
  
  // 发布配置
  location?: string;         // 所在地
  freight?: number;          // 运费
  warranty?: string;         // 保修
}

export interface PublishResult {
  success: boolean;
  itemId?: string;           // 淘宝商品 ID
  error?: string;
  warnings?: string[];
}
