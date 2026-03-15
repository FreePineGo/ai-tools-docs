#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析 Agent - 演示脚本（离线测试用）
"""

import sys
import os
sys.path.insert(0, 'src')

from analyzer import StockAnalyzer
from report_generator import ReportGenerator

def demo():
    print("=" * 60)
    print("📊 股票分析 Agent - 演示模式".center(60))
    print("=" * 60)
    
    # 初始化
    analyzer = StockAnalyzer('config.json')
    
    # 测试股票
    test_stocks = [
        {'code': '600519', 'name': '贵州茅台', 'market': 'SH'},
        {'code': '000858', 'name': '五粮液', 'market': 'SZ'},
        {'code': '601857', 'name': '中国石油', 'market': 'SH'}
    ]
    
    results = []
    
    for stock in test_stocks:
        print(f"\n分析 {stock['name']} ({stock['code']})...")
        result = analyzer.analyze_stock(stock)
        results.append(result)
        
        rating = result.get('rating', {})
        icon = {'强烈推荐': '🟢', '推荐': '🟡', '中性': '⚪', '谨慎': '🟠', '回避': '🔴'}.get(rating.get('rating'), '⚪')
        
        print(f"  {icon} 评级：{rating.get('rating', '未知')} ({rating.get('score', 0)}分)")
        
        tech = result.get('technical', {})
        if tech and not tech.get('error'):
            print(f"     趋势：{tech.get('trend', '未知')}")
            signals = tech.get('signals', [])
            if signals:
                for s in signals[:2]:
                    print(f"     - {s.get('desc', '')}")
        
        fund = result.get('fundamental', {})
        if fund and not fund.get('error'):
            print(f"     基本面：{fund.get('evaluation', '')}")
    
    # 生成报告
    print("\n" + "=" * 60)
    print("生成报告...")
    
    report_gen = ReportGenerator('reports')
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    
    # 模拟舆情数据
    sentiment_results = [
        {
            'stock_code': r['stock_code'],
            'stock_name': r['name'],
            'sentiment': {
                'sentiment': 'positive' if r['rating']['score'] > 60 else 'neutral',
                'score': 0.6 + (r['rating']['score'] - 50) / 100,
                'news_count': 10,
                'positive_count': 6,
                'negative_count': 2
            }
        }
        for r in results
    ]
    
    report_path = report_gen.generate_daily_report(results, sentiment_results, date)
    print(f"报告已保存：{report_path}")
    
    print("\n✅ 演示完成!")
    print(f"\n查看报告：{report_path}")

if __name__ == '__main__':
    demo()
