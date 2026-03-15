#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析 Agent - 主入口（基于 AkShare）
支持命令行运行和 API 调用
"""

import sys
import os
import json
import argparse
from datetime import datetime

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analyzer import StockAnalyzer, HAS_AK
from news_monitor import NewsMonitor
from report_generator import ReportGenerator


def run_analysis(config_path: str = 'config.json', output_dir: str = 'reports'):
    """执行完整分析流程"""
    
    print("=" * 60)
    print("📊 股票分析 Agent (AkShare)".center(60))
    print("=" * 60)
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not HAS_AK:
        print("❌ 错误：akshare 未安装")
        print("   请运行：pip install akshare")
        return None
    
    # 初始化
    analyzer = StockAnalyzer(config_path)
    news_monitor = NewsMonitor(os.path.join(os.path.dirname(__file__), 'news_cache'))
    report_gen = ReportGenerator(output_dir)
    
    # 加载配置
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
        config = {'stocks': []}
    
    stocks = config.get('stocks', [])
    print(f"监控股票：{len(stocks)} 只")
    for s in stocks:
        print(f"  - {s.get('name', '')} ({s['code']})")
    print()
    
    # 执行分析
    print("📈 执行技术分析 + 基本面分析...")
    analysis_results = analyzer.analyze_all()
    
    print("\n📰 执行舆情监控...")
    use_cache = config.get('analysis', {}).get('sentiment', {}).get('enabled', True)
    cache_hours = config.get('analysis', {}).get('sentiment', {}).get('cache_hours', 2)
    sentiment_results = news_monitor.monitor_all(stocks, use_cache=use_cache, cache_hours=cache_hours)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("📋 分析摘要")
    print("=" * 60)
    
    for result in analysis_results:
        name = result.get('name', '')
        code = result.get('stock_code', '')
        rating = result.get('rating', {})
        
        rating_text = rating.get('rating', '未知')
        score = rating.get('score', 0)
        
        # 图标
        icon_map = {'强烈推荐': '🟢', '推荐': '🟡', '中性': '⚪', '谨慎': '🟠', '回避': '🔴'}
        icon = icon_map.get(rating_text, '⚪')
        
        print(f"\n{icon} {name} ({code})")
        print(f"   评级：{rating_text} ({score}分)")
        
        # 技术信号
        tech = result.get('technical', {})
        if tech and not tech.get('error'):
            signals = tech.get('signals', [])
            trend = tech.get('trend', '')
            if trend:
                print(f"   趋势：{trend}")
            if signals:
                print(f"   技术信号：{len(signals)} 个")
                for s in signals[:3]:
                    print(f"     - {s.get('desc', '')}")
        
        # 基本面
        fund = result.get('fundamental', {})
        if fund and not fund.get('error'):
            eval_text = fund.get('evaluation', '')
            fund_score = fund.get('scores', {}).get('total', 0)
            print(f"   基本面：{eval_text} ({fund_score}分)")
        
        # 舆情
        sent_result = next((s for s in sentiment_results if s.get('stock_code') == code), None)
        if sent_result:
            sent = sent_result.get('sentiment', {})
            sent_text = sent.get('sentiment', 'neutral')
            sent_icon_map = {'positive': '😊', 'negative': '😟', 'neutral': '😐'}
            sent_icon = sent_icon_map.get(sent_text, '😐')
            print(f"   舆情：{sent_icon} {sent_text} ({sent.get('score', 0)})")
    
    # 生成报告
    print("\n" + "=" * 60)
    print("📝 生成报告...")
    print("=" * 60)
    
    date = datetime.now().strftime('%Y-%m-%d')
    report_path = report_gen.generate_daily_report(analysis_results, sentiment_results, date)
    print(f"报告已保存：{report_path}")
    
    # 输出 JSON 结果（用于 API 调用）
    output_json = {
        'timestamp': datetime.now().isoformat(),
        'stocks_analyzed': len(analysis_results),
        'results': analysis_results,
        'sentiment': sentiment_results,
        'report_path': report_path
    }
    
    json_path = os.path.join(output_dir, f'analysis_result_{date}.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=2)
    
    print(f"JSON 结果：{json_path}")
    
    print("\n✅ 分析完成!")
    
    return output_json


def analyze_single_stock(code: str, name: str = ''):
    """分析单只股票"""
    if not HAS_AK:
        print("❌ 错误：akshare 未安装")
        print("   请运行：pip install akshare")
        return None
    
    analyzer = StockAnalyzer()
    
    stock = {'code': code, 'name': name or code}
    result = analyzer.analyze_stock(stock)
    
    print(f"\n{name or code} ({code})")
    print(f"  评级：{result.get('rating', {}).get('rating', '未知')}")
    print(f"  评分：{result.get('rating', {}).get('score', 0)}分")
    
    return result


def main():
    parser = argparse.ArgumentParser(description='股票分析 Agent (AkShare)')
    
    parser.add_argument('--config', '-c', default='config.json',
                       help='配置文件路径')
    parser.add_argument('--output', '-o', default='reports',
                       help='输出目录')
    parser.add_argument('--stock', '-s', metavar='CODE',
                       help='分析单只股票（代码）')
    parser.add_argument('--name', '-n', default='',
                       help='股票名称（与--stock 配合使用）')
    parser.add_argument('--json', action='store_true',
                       help='仅输出 JSON 结果')
    parser.add_argument('--no-cache', action='store_true',
                       help='不使用缓存（获取最新舆情）')
    
    args = parser.parse_args()
    
    if args.stock:
        # 分析单只股票
        result = analyze_single_stock(args.stock, args.name)
        if args.json and result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 完整分析
        result = run_analysis(args.config, args.output)
        if args.json and result:
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
