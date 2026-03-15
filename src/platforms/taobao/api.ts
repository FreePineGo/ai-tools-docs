/**
 * 淘宝开放平台 API 封装
 * 基于 TOP SDK 的简化实现
 */

import axios from 'axios';
import * as crypto from 'crypto';

export interface TaobaoConfig {
  appKey: string;
  appSecret: string;
  accessToken: string;
  sandbox?: boolean;
}

export interface TaobaoResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: number;
    message: string;
    subCode?: string;
    subMsg?: string;
  };
}

export class TaobaoAPI {
  private config: TaobaoConfig;
  private baseUrl: string;

  constructor(config: TaobaoConfig) {
    this.config = config;
    this.baseUrl = config.sandbox 
      ? 'http://gw.api.tbsandbox.com/router/rest'
      : 'http://gw.api.taobao.com/router/rest';
  }

  /**
   * 生成签名
   */
  private sign(params: Record<string, string>): string {
    const sortedKeys = Object.keys(params).sort();
    const signString = this.config.appSecret + 
      sortedKeys.map(k => k + params[k]).join('') + 
      this.config.appSecret;
    
    return crypto
      .createHash('md5')
      .update(signString, 'utf8')
      .digest('hex')
      .toUpperCase();
  }

  /**
   * 执行 API 请求
   */
  async request<T>(method: string, params: Record<string, any>): Promise<TaobaoResponse<T>> {
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').substring(0, 19);
    
    const baseParams: Record<string, string> = {
      app_key: this.config.appKey,
      method,
      timestamp,
      v: '2.0',
      sign_method: 'md5',
      format: 'json',
      access_token: this.config.accessToken
    };

    // 添加业务参数
    Object.keys(params).forEach(key => {
      const value = params[key];
      baseParams[key] = typeof value === 'object' 
        ? JSON.stringify(value) 
        : String(value);
    });

    // 生成签名
    baseParams.sign = this.sign(baseParams);

    try {
      const response = await axios.post(this.baseUrl, new URLSearchParams(baseParams), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        timeout: 30000
      });

      const data = response.data;
      
      // 检查错误
      if (data.error_response) {
        return {
          success: false,
          error: {
            code: data.error_response.code,
            message: data.error_response.msg,
            subCode: data.error_response.sub_code,
            subMsg: data.error_response.sub_msg
          }
        };
      }

      // 提取响应数据（去掉方法名包裹）
      const responseKey = method.replace(/\./g, '_') + '_response';
      const result = data[responseKey];

      return {
        success: true,
        data: result as T
      };
    } catch (error: any) {
      return {
        success: false,
        error: {
          code: -1,
          message: error.message || '网络请求失败'
        }
      };
    }
  }

  /**
   * 获取商品类目
   */
  async getItemCats(parentCid: number = 0): Promise<any[]> {
    const result = await this.request<any>('taobao.itemcats.get', {
      parent_cid: parentCid,
      fields: 'cid,parent_cid,name,is_parent'
    });

    if (result.success && result.data) {
      return result.data.item_cats_get_response?.item_cats || [];
    }
    
    throw new Error(result.error?.message || '获取类目失败');
  }

  /**
   * 获取类目属性
   */
  async getItemProps(cid: number): Promise<any[]> {
    const result = await this.request<any>('taobao.itemprops.get', {
      cid,
      fields: 'pid,name,parent_pid,parent_value_id,prop_values'
    });

    if (result.success && result.data) {
      return result.data.itemprops_get_response?.item_props || [];
    }

    throw new Error(result.error?.message || '获取属性失败');
  }

  /**
   * 发布商品
   */
  async addItem(item: any): Promise<string> {
    const result = await this.request<any>('taobao.item.add', {
      title: item.title,
      desc: item.description,
      cid: item.categoryId,
      price: item.price,
      num: item.stock,
      location_state: item.location_state || '浙江',
      location_city: item.location_city || '杭州',
      express_fee: item.express_fee || 0,
      has_discount: item.has_discount || true,
      has_invoice: item.has_invoice || false,
      has_warranty: item.has_warranty || false,
      has_showcase: item.has_showcase || true,
      modified: new Date().toISOString(),
      increment: item.increment || '1',
      approve_status: item.approve_status || 'onsale',
      postage_id: item.postage_id,
      product_id: item.product_id,
      auction_point: item.auction_point || 0,
      property_alias: item.property_alias,
      template_id: item.template_id,
      outer_id: item.outer_id,
      is_virtual: item.is_virtual || false,
      is_taobao: item.is_taobao || false,
      is_ex: item.is_ex || false,
      is_timing: item.is_timing || false,
      second_kill: item.second_kill,
      auto_fill: item.auto_fill,
      props: item.props,
      input_pids: item.input_pids,
      input_str: item.input_str,
      pic_path: item.pic_path,
      num_iid: item.num_iid,
      locality_life: item.locality_life,
      skus: item.skus ? JSON.stringify(item.skus) : undefined,
      props_name: item.props_name
    });

    if (result.success && result.data) {
      const itemId = result.data.item_add_response?.item?.num_iid;
      if (itemId) {
        console.log(`[淘宝] 商品发布成功，ID: ${itemId}`);
        return itemId;
      }
    }

    throw new Error(result.error?.message || '发布商品失败');
  }

  /**
   * 更新商品
   */
  async updateItem(numIid: string, item: any): Promise<boolean> {
    const result = await this.request<any>('taobao.item.update', {
      num_iid: numIid,
      ...item
    });

    return result.success;
  }

  /**
   * 删除商品
   */
  async deleteItem(numIid: string): Promise<boolean> {
    const result = await this.request<any>('taobao.item.delete', {
      num_iid: numIid
    });

    return result.success;
  }

  /**
   * 获取商品信息
   */
  async getItem(numIid: string): Promise<any> {
    const result = await this.request<any>('taobao.item.get', {
      num_iid: numIid,
      fields: 'num_iid,title,desc,cid,price,num,location,skus,item_imgs,prop_img,props'
    });

    if (result.success && result.data) {
      return result.data.item_get_response?.item;
    }

    throw new Error(result.error?.message || '获取商品失败');
  }

  /**
   * 获取店铺商品列表
   */
  async getItems(pageNo: number = 1, pageSize: number = 20): Promise<any[]> {
    const result = await this.request<any>('taobao.items.list', {
      page_no: pageNo,
      page_size: pageSize,
      fields: 'num_iid,title,price,num,pic_url'
    });

    if (result.success && result.data) {
      return result.data.items_list_get_response?.items?.item || [];
    }

    throw new Error(result.error?.message || '获取商品列表失败');
  }

  /**
   * 上传图片到淘宝图片空间
   */
  async uploadImage(imagePath: string, imageType?: string): Promise<string> {
    // 淘宝图片上传需要使用专门的 API
    // 这里提供简化版本，实际使用需要 multipart/form-data
    
    const result = await this.request<any>('taobao.picture.upload', {
      image: imagePath,
      title: imagePath.split('/').pop(),
      image_type: imageType
    });

    if (result.success && result.data) {
      return result.data.picture_upload_response?.picture?.url;
    }

    throw new Error(result.error?.message || '上传图片失败');
  }
}
