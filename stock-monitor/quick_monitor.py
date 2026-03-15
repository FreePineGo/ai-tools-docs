#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简股票监控 - 单文件版本
无需配置，直接运行
"""

import requests
import time
from datetime import datetime

# 石油板块股票池
STOCKS = [
    {"code": "601857", "name": "中国石油", "market": "SH"},
    {"code": "600028", "name": "中国石化", "market": "SH"},
    {"code": "600938", "name": "中国海油", "market": "SH"},
    {"code": "601808", "name": "中海油服", "market": "SH"},
    {"code": "600583", "name": "海油工程", "market": "SH"},
    {"code": "002353", "name": "杰瑞股份", "market": "SZ"},
]

def get_stock_data(code: str, market: str) -> dict:
    """获取股票实时数据"""
    url = "http://push2.eastmoney.com/api/qt/stock/get"
    params = {
        'secid': f"{market}.{code}",
        'fields': 'f43,f44,f45,f46,f47,f48,f170,f171'
    }
    
    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()['data']
        
        return {
            'price': data['f43'] / 100,
            'open': data['f46'] / 100,
            'high': data['f44'] / 100,
            'low': data['f45'] / 100,
            'volume': data['f47'],
            'amount': data['f48'],
            'change': data['f170'] / 100,
            'change_pct': data['f171'] / 100,
        }
    except:
        return None

def display():
    """显示行情"""
    print("\n" + "="*70)
    print(f"📊 石油板块实时监控  {datetime.now().strftime('%H:%M:%S')}".center(70))
    print("="*70)
    print(f"{'股票':<10} {'代码':<8} {'现价':>8} {'涨跌':>8} {'涨幅%':>8} {'成交量':>12}")
    print("-"*70)
    
    for stock in STOCKS:
        data = get_stock_data(stock['code'], stock['market'])
        if data:
            change_icon = "📈" if data['change_pct'] > 0 else "📉" if data['change_pct'] < 0 else "➖"
            print(f"{stock['name']:<10} {stock['code']:<8} "
                  f"¥{data['price']:>6.2f} {data['change']:>+7.2f} "
                  f"{data['change_pct']:>+7.2f}% {data['volume']/10000:>10.1f}万手")
        else:
            print(f"{stock['name']:<10} {stock['code']:<8} {'获取失败':>15}")
        
        time.sleep(0.3)
    
    print("="*70)

def main():
    """主循环"""
    print("🚀 启动股票监控 (Ctrl+C 停止)")
    
    try:
        while True:
            display()
            print(f"\n⏱️  10 秒后刷新...")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\n👋 已停止监控")

if __name__ == '__main__':
    main()
