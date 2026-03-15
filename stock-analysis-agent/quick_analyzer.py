#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票快速分析 - 使用 AkShare 接口（更稳定）
"""

import sys
import os
from datetime import datetime

try:
    import akshare as ak
    import pandas as pd
    import numpy as np
    HAS_AK = True
except ImportError:
    HAS_AK = False
    print("未安装 akshare，运行：pip install akshare")


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """计算技术指标"""
    # MA
    for period in [5, 10, 20, 60]:
        df[f'MA{period}'] = df['close'].rolling(window=period).mean()
    
    # MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df


def analyze_stock_ak(symbol: str) -> dict:
    """使用 AkShare 分析股票"""
    if not HAS_AK:
        return {'error': 'akshare 未安装'}
    
    try:
        # 获取历史行情
        print(f"获取 {symbol} 行情数据...")
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20230101")
        
        if df.empty:
            return {'error': '无数据'}
        
        # 重命名列
        df = df.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'turnover',
            '振幅': 'amplitude',
            '涨跌幅': 'change_pct',
            '涨跌额': 'change',
            '换手率': 'turnover_rate'
        })
        
        # 计算指标
        df = calculate_indicators(df)
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # 生成信号
        signals = []
        
        # MA 金叉/死叉
        if latest['MA5'] > latest['MA10'] and prev['MA5'] <= prev['MA10']:
            signals.append({'type': 'golden_cross', 'signal': '买入', 'desc': 'MA5 上穿 MA10 金叉'})
        elif latest['MA5'] < latest['MA10'] and prev['MA5'] >= prev['MA10']:
            signals.append({'type': 'death_cross', 'signal': '卖出', 'desc': 'MA5 下穿 MA10 死叉'})
        
        # RSI
        if latest['RSI'] < 20:
            signals.append({'type': 'oversold', 'signal': '买入', 'desc': f'RSI 超卖 ({latest["RSI"]:.1f})'})
        elif latest['RSI'] > 80:
            signals.append({'type': 'overbought', 'signal': '卖出', 'desc': f'RSI 超买 ({latest["RSI"]:.1f})'})
        
        # 判断趋势
        if latest['close'] > latest['MA20'] > latest['MA60']:
            trend = '上升趋势'
        elif latest['close'] < latest['MA20'] < latest['MA60']:
            trend = '下降趋势'
        else:
            trend = '震荡'
        
        # 综合评分
        score = 50
        if trend == '上升趋势':
            score += 20
        elif trend == '下降趋势':
            score -= 20
        
        buy_signals = sum(1 for s in signals if s['signal'] == '买入')
        sell_signals = sum(1 for s in signals if s['signal'] == '卖出')
        score += (buy_signals - sell_signals) * 15
        
        # 评级
        if score >= 80:
            rating = '强烈推荐'
        elif score >= 65:
            rating = '推荐'
        elif score >= 50:
            rating = '中性'
        elif score >= 35:
            rating = '谨慎'
        else:
            rating = '回避'
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price': latest['close'],
            'change_pct': latest['change_pct'],
            'trend': trend,
            'indicators': {
                'MA5': round(latest['MA5'], 2),
                'MA10': round(latest['MA10'], 2),
                'MA20': round(latest['MA20'], 2),
                'MA60': round(latest['MA60'], 2),
                'RSI': round(latest['RSI'], 2) if not np.isnan(latest['RSI']) else 50
            },
            'signals': signals,
            'rating': {
                'score': round(score, 1),
                'rating': rating
            }
        }
        
    except Exception as e:
        return {'error': str(e)}


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='股票快速分析')
    parser.add_argument('symbol', nargs='?', default='600519', help='股票代码')
    args = parser.parse_args()
    
    print("=" * 60)
    print("📊 股票快速分析 (AkShare)".center(60))
    print("=" * 60)
    
    result = analyze_stock_ak(args.symbol)
    
    if 'error' in result:
        print(f"❌ 错误：{result['error']}")
        return
    
    print(f"\n{result.get('symbol', '未知')}")
    print(f"   当前价：{result.get('price', 0)}")
    print(f"   涨跌幅：{result.get('change_pct', 0):.2f}%")
    print(f"   趋势：{result.get('trend', '未知')}")
    print(f"   评级：{result.get('rating', {}).get('rating', '未知')} ({result.get('rating', {}).get('score', 0)}分)")
    
    print("\n技术指标:")
    for k, v in result.get('indicators', {}).items():
        print(f"   {k}: {v}")
    
    print("\n信号:")
    signals = result.get('signals', [])
    if signals:
        for s in signals:
            icon = '📈' if s['signal'] == '买入' else '📉' if s['signal'] == '卖出' else '⏸️'
            print(f"   {icon} {s['desc']}")
    else:
        print("   无明显信号")


if __name__ == '__main__':
    main()
