#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票新闻舆情监控模块 - 基于 AkShare
抓取并分析股票相关新闻、公告、舆情
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import time

try:
    import akshare as ak
    import pandas as pd
    HAS_AK = True
except ImportError:
    HAS_AK = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NewsMonitor:
    """新闻舆情监控器 - 使用 AkShare"""
    
    def __init__(self, cache_dir: str = 'news_cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def fetch_company_news(self, stock_code: str, page_size: int = 20) -> List[Dict]:
        """
        获取个股新闻（使用 AkShare）
        
        Args:
            stock_code: 股票代码
            page_size: 新闻数量
        """
        if not HAS_AK:
            return []
        
        try:
            # 获取个股新闻
            df = ak.stock_news_em(symbol=stock_code)
            
            if df is None or df.empty:
                return []
            
            news_list = []
            for _, row in df.head(page_size).iterrows():
                news_list.append({
                    'title': row.get('新闻标题', ''),
                    'content': row.get('新闻内容', '')[:300],
                    'source': row.get('文章来源', '东方财富'),
                    'publish_time': row.get('发布时间', ''),
                    'url': row.get('新闻链接', ''),
                    'type': 'news'
                })
            
            return news_list
            
        except Exception as e:
            logger.error(f"获取新闻失败 {stock_code}: {e}")
            return []
    
    def fetch_announcements(self, stock_code: str, page_size: int = 10) -> List[Dict]:
        """
        获取公司公告（使用 AkShare）
        
        Args:
            stock_code: 股票代码
            page_size: 公告数量
        """
        if not HAS_AK:
            return []
        
        try:
            # 获取公司公告
            df = ak.stock_notice_report(symbol=stock_code)
            
            if df is None or df.empty:
                return []
            
            news_list = []
            for _, row in df.head(page_size).iterrows():
                news_list.append({
                    'title': row.get('公告标题', ''),
                    'content': row.get('公告内容', '')[:300],
                    'source': '公司公告',
                    'publish_time': row.get('公告时间', ''),
                    'url': row.get('公告链接', ''),
                    'type': 'announcement'
                })
            
            return news_list
            
        except Exception as e:
            logger.error(f"获取公告失败 {stock_code}: {e}")
            return []
    
    def analyze_sentiment(self, news_list: List[Dict]) -> Dict:
        """
        分析新闻情绪
        
        Returns:
            情绪分析结果
        """
        if not news_list:
            return {'sentiment': 'neutral', 'score': 0.5, 'news_count': 0}
        
        positive_words = [
            '增长', '上涨', '利好', '突破', '创新高', '业绩', '盈利', '分红',
            '重组', '并购', '扩张', '订单', '签约', '合作', '获奖', '领先',
            '预增', '扭亏', '回购', '增持', '中标', '突破', '放量'
        ]
        
        negative_words = [
            '下跌', '亏损', '下滑', '风险', '警告', '处罚', '诉讼', '减持',
            '退市', '暴雷', '违约', '调查', '整改', '延期', '取消', '失败',
            '预亏', '下降', '缩水', '暴跌', '跌停', '立案', '警示'
        ]
        
        positive_count = 0
        negative_count = 0
        
        for news in news_list:
            text = (news.get('title', '') + ' ' + news.get('content', '')).lower()
            
            for word in positive_words:
                if word in text:
                    positive_count += 1
            
            for word in negative_words:
                if word in text:
                    negative_count += 1
        
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.5
        else:
            sentiment_score = positive_count / total
        
        # 判断情绪
        if sentiment_score > 0.6:
            sentiment = 'positive'
        elif sentiment_score < 0.4:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'score': round(sentiment_score, 2),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'news_count': len(news_list),
            'latest_news': news_list[:5] if news_list else []
        }
    
    def monitor_stock(self, stock_code: str, stock_name: str = '') -> Dict:
        """
        监控单只股票的舆情
        
        Returns:
            舆情分析结果
        """
        logger.info(f"监控 {stock_name or stock_code} 舆情...")
        
        # 获取新闻
        news_list = []
        
        # 个股新闻
        company_news = self.fetch_company_news(stock_code)
        news_list.extend(company_news)
        
        # 公司公告
        announcements = self.fetch_announcements(stock_code)
        news_list.extend(announcements)
        
        # 去重
        seen_urls = set()
        unique_news = []
        for news in news_list:
            url = news.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(news)
            elif not url:
                unique_news.append(news)
        
        # 分析情绪
        sentiment_result = self.analyze_sentiment(unique_news)
        
        # 保存到缓存
        self._save_cache(stock_code, {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'news': unique_news[:20],
            'sentiment': sentiment_result
        })
        
        return {
            'stock_code': stock_code,
            'stock_name': stock_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'news_count': len(unique_news),
            'sentiment': sentiment_result
        }
    
    def _save_cache(self, stock_code: str, data: Dict):
        """保存缓存"""
        cache_file = os.path.join(self.cache_dir, f'{stock_code}_news.json')
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_cache(self, stock_code: str, cache_hours: int = 2) -> Optional[Dict]:
        """加载缓存（如果在有效期内）"""
        cache_file = os.path.join(self.cache_dir, f'{stock_code}_news.json')
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cache_time = datetime.strptime(data.get('timestamp', ''), '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cache_time < timedelta(hours=cache_hours):
                return data
        except Exception as e:
            logger.error(f"加载缓存失败：{e}")
        
        return None
    
    def monitor_all(self, stocks: List[Dict], use_cache: bool = True, 
                    cache_hours: int = 2) -> List[Dict]:
        """监控所有股票舆情"""
        results = []
        
        for stock in stocks:
            # 尝试加载缓存
            if use_cache:
                cached = self.load_cache(stock['code'], cache_hours)
                if cached:
                    logger.info(f"使用缓存数据：{stock.get('name', stock['code'])}")
                    results.append({
                        'stock_code': stock['code'],
                        'stock_name': stock.get('name', ''),
                        'from_cache': True,
                        **cached['sentiment']
                    })
                    continue
            
            # 获取新数据
            result = self.monitor_stock(stock['code'], stock.get('name', ''))
            results.append(result)
            
            time.sleep(1)  # 避免请求过快
        
        return results


if __name__ == '__main__':
    # 测试
    if not HAS_AK:
        print("请先安装 akshare: pip install akshare")
    else:
        monitor = NewsMonitor()
        
        stocks = [
            {'code': '601857', 'name': '中国石油'},
            {'code': '600519', 'name': '贵州茅台'}
        ]
        
        results = monitor.monitor_all(stocks, use_cache=False)
        
        for r in results:
            print(f"\n{r['stock_name']} ({r['stock_code']})")
            print(f"  新闻数量：{r.get('news_count', 0)}")
            print(f"  情绪：{r.get('sentiment', {}).get('sentiment', 'unknown')}")
            print(f"  情绪分数：{r.get('sentiment', {}).get('score', 0)}")
