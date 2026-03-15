/**
 * 类目和属性映射模块
 * 将 1688 类目映射到淘宝类目
 */

import { Product } from '../../core/product.js';

/**
 * 1688 类目到淘宝类目的映射
 * 这是一个简化版本，实际需要更完整的映射表
 */
const CATEGORY_MAP: Record<string, number> = {
  // 服装
  '女装': 50000671,
  '男装': 30,
  '童装': 50008897,
  '内衣': 50006842,
  
  // 鞋包
  '女鞋': 50006843,
  '男鞋': 50012027,
  '箱包': 50006844,
  
  // 数码
  '手机': 50003241,
  '电脑': 50003109,
  '数码配件': 50013194,
  
  // 家居
  '家纺': 50003322,
  '家居用品': 50008163,
  '厨具': 50008164,
  
  // 美妆
  '美妆': 50010788,
  '个护': 50011972,
  '香水': 50011973,
  
  // 食品
  '零食': 50012082,
  '茶叶': 50002766,
  '酒类': 50008090,
  
  // 母婴
  '奶粉': 50014812,
  '纸尿裤': 50014808,
  '玩具': 50012622,
  
  // 运动
  '运动服饰': 50014865,
  '运动鞋': 50011740,
  '健身器材': 50015012
};

/**
 * 属性映射配置
 */
interface PropMapping {
  sourceProp: string;      // 1688 属性名
  targetProp: string;      // 淘宝属性名
  valueMap?: Record<string, string>;  // 值映射
}

/**
 * 类目属性映射
 */
const PROP_MAPPINGS: Record<number, PropMapping[]> = {
  50000671: [  // 女装
    { sourceProp: '颜色', targetProp: '颜色分类' },
    { sourceProp: '尺码', targetProp: '尺码' },
    { sourceProp: '材质', targetProp: '材质成分' },
    { sourceProp: '风格', targetProp: '风格' }
  ],
  30: [  // 男装
    { sourceProp: '颜色', targetProp: '颜色分类' },
    { sourceProp: '尺码', targetProp: '尺码' },
    { sourceProp: '材质', targetProp: '材质' }
  ]
};

export class TaobaoMapper {
  /**
   * 映射类目
   */
  async mapCategory(sourceCategory: string, taobaoAPI?: any): Promise<number> {
    // 1. 尝试从映射表查找
    for (const [key, cid] of Object.entries(CATEGORY_MAP)) {
      if (sourceCategory.includes(key)) {
        console.log(`[映射] 类目匹配：${sourceCategory} -> ${cid}`);
        return cid;
      }
    }

    // 2. 如果提供了淘宝 API，搜索匹配的类目
    if (taobaoAPI) {
      const cats = await taobaoAPI.getItemCats(0);
      const matched = cats.find((c: any) => 
        c.name.includes(sourceCategory) || sourceCategory.includes(c.name)
      );
      
      if (matched) {
        console.log(`[映射] API 类目匹配：${sourceCategory} -> ${matched.cid}`);
        return matched.cid;
      }
    }

    // 3. 默认返回一个通用类目
    console.warn(`[映射] 未找到类目映射，使用默认类目：50000671 (女装)`);
    return 50000671;
  }

  /**
   * 映射属性
   */
  mapProperties(product: Product, categoryId: number): Record<string, string> {
    const mappings = PROP_MAPPINGS[categoryId] || [];
    const result: Record<string, string> = {};

    // 复制原始属性
    Object.assign(result, product.properties);

    // 应用映射
    for (const mapping of mappings) {
      const sourceValue = product.properties[mapping.sourceProp];
      if (sourceValue) {
        const targetValue = mapping.valueMap?.[sourceValue] || sourceValue;
        result[mapping.targetProp] = targetValue;
        delete result[mapping.sourceProp];
      }
    }

    return result;
  }

  /**
   * 映射 SKU 属性
   */
  mapSKUProperties(skus: any[], categoryId: number): any[] {
    const mappings = PROP_MAPPINGS[categoryId] || [];
    
    return skus.map(sku => {
      const mapped = { ...sku };
      
      for (const mapping of mappings) {
        if (mapped.properties && typeof mapped.properties === 'string') {
          mapped.properties = mapped.properties.replace(
            mapping.sourceProp,
            mapping.targetProp
          );
        }
      }
      
      return mapped;
    });
  }

  /**
   * 转换商品格式（1688 -> 淘宝）
   */
  async convertToTaobaoFormat(product: Product, taobaoAPI?: any): Promise<any> {
    // 映射类目
    const categoryId = await this.mapCategory(
      product.properties['类目'] || product.title,
      taobaoAPI
    );

    // 映射属性
    const properties = this.mapProperties(product, categoryId);

    // 映射 SKU
    const skus = this.mapSKUProperties(product.skus, categoryId);

    // 构建淘宝商品数据
    const taobaoItem: any = {
      title: this.optimizeTitle(product.title),
      description: this.formatDescription(product),
      categoryId,
      price: this.adjustPrice(product.price),
      stock: product.stock,
      skus: skus.map(s => ({
        properties_name: s.properties,
        price: s.price,
        quantity: s.stock
      })),
      properties: this.formatProperties(properties),
      location_state: product.location?.split(' ')[0] || '浙江',
      location_city: product.location?.split(' ')[1] || '杭州',
      express_fee: product.freight || 0,
      has_discount: true,
      has_invoice: false,
      has_warranty: product.warranty ? true : false,
      has_showcase: true,
      approve_status: 'onsale',  // 立即上架
      outer_id: `1688_${Date.now()}`,  // 商家编码
      is_virtual: false,
      is_timing: false
    };

    // 处理图片
    if (product.images && product.images.length > 0) {
      // 主图
      const mainImages = product.images.filter((img: any) => img.type === 'main');
      if (mainImages.length > 0) {
        taobaoItem.pic_path = mainImages[0].url;
      }
      
      // 详情图（需要上传到图片空间后使用）
      // taobaoItem.item_imgs = ...
    }

    return taobaoItem;
  }

  /**
   * 优化标题（符合淘宝规范）
   */
  private optimizeTitle(title: string): string {
    // 去除特殊字符
    title = title.replace(/[<>\"\'\\]/g, '');
    
    // 限制长度（淘宝标题最多 60 字符）
    if (title.length > 60) {
      title = title.substring(0, 57) + '...';
    }
    
    return title;
  }

  /**
   * 格式化描述
   */
  private formatDescription(product: Product): string {
    let desc = product.description || '';
    
    // 添加图片
    const detailImages = product.images?.filter((img: any) => img.type === 'detail') || [];
    if (detailImages.length > 0) {
      desc += '\n\n';
      desc += detailImages.map((img: any) => `<img src="${img.url}" />`).join('\n');
    }
    
    // 限制长度
    if (desc.length > 50000) {
      desc = desc.substring(0, 49997) + '...';
    }
    
    return desc;
  }

  /**
   * 调整价格（考虑利润率）
   */
  private adjustPrice(sourcePrice: number, profitMargin: number = 0.2): number {
    // 默认加价 20%
    const price = sourcePrice * (1 + profitMargin);
    return Math.round(price * 100) / 100;
  }

  /**
   * 格式化属性字符串（淘宝格式：pid:vid;pid:vid）
   */
  private formatProperties(properties: Record<string, string>): string {
    // 这里需要实际的属性 ID 映射
    // 简化版本：直接返回属性名值对
    return Object.entries(properties)
      .map(([key, value]) => `${key}:${value}`)
      .join(';');
  }
}

export const mapper = new TaobaoMapper();
