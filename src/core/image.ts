/**
 * 图片处理模块
 * 下载、压缩、格式转换
 */

import axios from 'axios';
import sharp from 'sharp';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';

export interface ImageOptions {
  maxWidth?: number;         // 最大宽度
  maxHeight?: number;        // 最大高度
  quality?: number;          // 质量 (1-100)
  format?: 'jpeg' | 'png' | 'webp';
}

const DEFAULT_OPTIONS: ImageOptions = {
  maxWidth: 800,
  maxHeight: 800,
  quality: 85,
  format: 'jpeg'
};

/**
 * 下载图片
 */
export async function downloadImage(url: string, outputPath: string): Promise<string> {
  const response = await axios({
    url,
    method: 'GET',
    responseType: 'stream'
  });

  const writer = createWriteStream(outputPath);
  await pipeline(response.data, writer);
  
  return outputPath;
}

/**
 * 处理图片（压缩、转换格式）
 */
export async function processImage(
  inputPath: string, 
  outputPath: string,
  options: ImageOptions = DEFAULT_OPTIONS
): Promise<string> {
  let processor = sharp(inputPath);
  
  // 调整尺寸
  if (options.maxWidth || options.maxHeight) {
    processor = processor.resize(options.maxWidth, options.maxHeight, {
      fit: 'inside',
      withoutEnlargement: true
    });
  }
  
  // 格式转换和压缩
  switch (options.format) {
    case 'jpeg':
      processor = processor.jpeg({ quality: options.quality });
      break;
    case 'png':
      processor = processor.png({ quality: options.quality });
      break;
    case 'webp':
      processor = processor.webp({ quality: options.quality });
      break;
  }
  
  await processor.toFile(outputPath);
  
  return outputPath;
}

/**
 * 下载并处理图片
 */
export async function downloadAndProcess(
  url: string, 
  outputPath: string,
  options: ImageOptions = DEFAULT_OPTIONS
): Promise<string> {
  const tempPath = outputPath + '.tmp';
  
  try {
    // 下载
    await downloadImage(url, tempPath);
    
    // 处理
    await processImage(tempPath, outputPath, options);
    
    // 清理临时文件
    import('fs/promises').then(fs => fs.unlink(tempPath));
    
    return outputPath;
  } catch (error) {
    console.error(`图片处理失败：${url}`, error);
    throw error;
  }
}
