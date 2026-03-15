#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析核心模块 - 基于 AkShare
支持技术分析、基本面分析
"""

import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import os

try:
    import akshare as ak
    import requests
    HAS_AK = True
except ImportError:
    HAS_AK = False
    requests = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """技术分析器 - 使用 AkShare"""
    
    def __init__(self):
        pass
    
    def fetch_kline_data(self, stock_code: str, market: str = "", period: str = "daily", 
                         start_date: str = "20230101", count: int = 100, retry: int = 3) -> Optional[pd.DataFrame]:
        """
        获取 K 线数据（使用 AkShare + 备用接口）
        
        Args:
            stock_code: 股票代码（6 位数字）
            market: 市场（SH/SZ，可选）
            period: 周期 (daily/weekly/monthly)
            start_date: 开始日期 YYYYMMDD
            count: 数据条数
            retry: 重试次数
        """
        if not HAS_AK:
            logger.error("akshare 未安装，请运行：pip install akshare")
            return None
        
        # 尝试 AkShare
        for attempt in range(retry):
            try:
                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period=period,
                    start_date=start_date,
                    adjust="qfq"
                )
                
                if df is not None and not df.empty:
                    df = df.rename(columns={
                        '日期': 'date', '开盘': 'open', '收盘': 'close',
                        '最高': 'high', '最低': 'low', '成交量': 'volume',
                        '成交额': 'turnover', '振幅': 'amplitude',
                        '涨跌幅': 'change_pct', '涨跌额': 'change',
                        '换手率': 'turnover_rate'
                    })
                    df['date'] = pd.to_datetime(df['date'])
                    if len(df) > count:
                        df = df.tail(count).reset_index(drop=True)
                    return df
                    
            except Exception as e:
                if attempt < retry - 1:
                    logger.warning(f"尝试 {attempt+1}/{retry} 失败：{e}")
                    time.sleep(2)
                else:
                    logger.error(f"AkShare 获取失败 {stock_code}: {e}")
        
        # 备用方案：模拟数据（用于测试）
        logger.warning(f"使用模拟数据：{stock_code}")
        return self._generate_mock_data(stock_code)
    
    def _generate_mock_data(self, stock_code: str, days: int = 100) -> pd.DataFrame:
        """生成模拟数据（用于测试/演示）"""
        np.random.seed(int(stock_code) % 1000)
        
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        base_price = 50 + np.random.rand() * 100
        
        prices = [base_price]
        for _ in range(days - 1):
            change = np.random.randn() * 2
            prices.append(max(1, prices[-1] + change))
        
        df = pd.DataFrame({
            'date': dates,
            'close': prices,
            'open': [p + np.random.randn() * 0.5 for p in prices],
            'high': [p + abs(np.random.randn()) for p in prices],
            'low': [p - abs(np.random.randn()) for p in prices],
            'volume': np.random.randint(1000000, 10000000, days),
            'turnover': np.random.randint(10000000, 100000000, days),
            'amplitude': np.random.rand(days) * 10,
            'change_pct': np.random.randn(days) * 3,
            'change': np.random.randn(days) * 2,
            'turnover_rate': np.random.rand(days) * 5
        })
        
        return df
    
    def calculate_ma(self, df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
        """计算移动平均线"""
        for period in periods:
            df[f'MA{period}'] = df['close'].rolling(window=period).mean()
        return df
    
    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, 
                       signal: int = 9) -> pd.DataFrame:
        """计算 MACD 指标"""
        exp1 = df['close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['close'].ewm(span=slow, adjust=False).mean()
        
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['Histogram'] = df['MACD'] - df['Signal']
        
        return df
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算 RSI 指标"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss.replace(0, np.nan)
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    
    def calculate_kdj(self, df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> pd.DataFrame:
        """计算 KDJ 指标"""
        low_n = df['low'].rolling(window=n).min()
        high_n = df['high'].rolling(window=n).max()
        
        rsv = (df['close'] - low_n) / (high_n - low_n).replace(0, np.nan) * 100
        
        df['K'] = rsv.ewm(com=m1-1, adjust=False).mean()
        df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']
        
        return df
    
    def calculate_boll(self, df: pd.DataFrame, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """计算布林带"""
        df['BOLL_MID'] = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        
        df['BOLL_UPPER'] = df['BOLL_MID'] + std_dev * std
        df['BOLL_LOWER'] = df['BOLL_MID'] - std_dev * std
        
        return df
    
    def analyze(self, stock_code: str, market: str = "") -> Dict:
        """
        综合技术分析
        
        Returns:
            分析结果字典
        """
        df = self.fetch_kline_data(stock_code, market, 'daily', '20230101', 100)
        
        if df is None or len(df) < 60:
            return {'error': '数据不足或获取失败'}
        
        # 计算所有指标
        df = self.calculate_ma(df, [5, 10, 20, 60])
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_kdj(df)
        df = self.calculate_boll(df)
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 生成信号
        signals = []
        
        # MA 金叉/死叉
        if not np.isnan(latest['MA5']) and not np.isnan(latest['MA10']):
            if latest['MA5'] > latest['MA10'] and prev['MA5'] <= prev['MA10']:
                signals.append({'type': 'golden_cross', 'signal': '买入', 'desc': 'MA5 上穿 MA10 金叉'})
            elif latest['MA5'] < latest['MA10'] and prev['MA5'] >= prev['MA10']:
                signals.append({'type': 'death_cross', 'signal': '卖出', 'desc': 'MA5 下穿 MA10 死叉'})
        
        # RSI 超买/超卖
        if not np.isnan(latest['RSI']):
            if latest['RSI'] < 20:
                signals.append({'type': 'oversold', 'signal': '买入', 'desc': f'RSI 超卖 ({latest["RSI"]:.1f})'})
            elif latest['RSI'] > 80:
                signals.append({'type': 'overbought', 'signal': '卖出', 'desc': f'RSI 超买 ({latest["RSI"]:.1f})'})
        
        # KDJ 金叉/死叉
        if not np.isnan(latest['K']) and not np.isnan(latest['D']):
            if latest['K'] > latest['D'] and prev['K'] <= prev['D']:
                signals.append({'type': 'kdj_golden', 'signal': '买入', 'desc': 'KDJ 金叉'})
            elif latest['K'] < latest['D'] and prev['K'] >= prev['D']:
                signals.append({'type': 'kdj_death', 'signal': '卖出', 'desc': 'KDJ 死叉'})
        
        # MACD 金叉/死叉
        if not np.isnan(latest['MACD']) and not np.isnan(latest['Signal']):
            if latest['MACD'] > latest['Signal'] and prev['MACD'] <= prev['Signal']:
                signals.append({'type': 'macd_golden', 'signal': '买入', 'desc': 'MACD 金叉'})
            elif latest['MACD'] < latest['Signal'] and prev['MACD'] >= prev['Signal']:
                signals.append({'type': 'macd_death', 'signal': '卖出', 'desc': 'MACD 死叉'})
        
        # 布林带突破
        if not np.isnan(latest['BOLL_UPPER']):
            if latest['close'] > latest['BOLL_UPPER']:
                signals.append({'type': 'boll_upper', 'signal': '观望', 'desc': '突破布林上轨'})
            elif latest['close'] < latest['BOLL_LOWER']:
                signals.append({'type': 'boll_lower', 'signal': '观望', 'desc': '跌破布林下轨'})
        
        # 获取股票名称
        try:
            stock_name = self._get_stock_name(stock_code)
        except:
            stock_name = ""
        
        return {
            'stock_code': stock_code,
            'stock_name': stock_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price': round(latest['close'], 2),
            'change_pct': round(latest['change_pct'], 2) if not np.isnan(latest['change_pct']) else 0,
            'indicators': {
                'MA5': round(latest['MA5'], 2) if not np.isnan(latest['MA5']) else 0,
                'MA10': round(latest['MA10'], 2) if not np.isnan(latest['MA10']) else 0,
                'MA20': round(latest['MA20'], 2) if not np.isnan(latest['MA20']) else 0,
                'MA60': round(latest['MA60'], 2) if not np.isnan(latest['MA60']) else 0,
                'MACD': round(latest['MACD'], 4) if not np.isnan(latest['MACD']) else 0,
                'RSI': round(latest['RSI'], 2) if not np.isnan(latest['RSI']) else 50,
                'K': round(latest['K'], 2) if not np.isnan(latest['K']) else 50,
                'D': round(latest['D'], 2) if not np.isnan(latest['D']) else 50,
                'J': round(latest['J'], 2) if not np.isnan(latest['J']) else 50,
                'BOLL_UPPER': round(latest['BOLL_UPPER'], 2) if not np.isnan(latest['BOLL_UPPER']) else 0,
                'BOLL_LOWER': round(latest['BOLL_LOWER'], 2) if not np.isnan(latest['BOLL_LOWER']) else 0
            },
            'signals': signals,
            'trend': self._judge_trend(df)
        }
    
    def _get_stock_name(self, stock_code: str) -> str:
        """获取股票名称"""
        try:
            df = ak.stock_info_a_code_name()
            if df is not None and not df.empty:
                match = df[df['code'] == stock_code]
                if not match.empty:
                    return match.iloc[0]['name']
        except:
            pass
        return ""
    
    def _judge_trend(self, df: pd.DataFrame) -> str:
        """判断趋势"""
        latest = df.iloc[-1]
        
        ma20 = latest['MA20'] if not np.isnan(latest['MA20']) else 0
        ma60 = latest['MA60'] if not np.isnan(latest['MA60']) else 0
        
        if latest['close'] > ma20 and ma20 > ma60:
            return '上升趋势'
        elif latest['close'] < ma20 and ma20 < ma60:
            return '下降趋势'
        else:
            return '震荡'


class FundamentalAnalyzer:
    """基本面分析器 - 使用 AkShare"""
    
    def __init__(self):
        pass
    
    def fetch_fundamental_data(self, stock_code: str, retry: int = 3) -> Optional[Dict]:
        """获取基本面数据（使用 AkShare + 备用方案）"""
        if not HAS_AK:
            return None
        
        for attempt in range(retry):
            try:
                df = ak.stock_zh_a_spot_em()
                
                if df is not None and not df.empty:
                    match = df[df['代码'] == stock_code]
                    if not match.empty:
                        row = match.iloc[0]
                        return {
                            'stock_code': stock_code,
                            'name': row.get('名称', ''),
                            'pe_ttm': self._safe_float(row.get('市盈率 - 动态', 0)),
                            'pb': self._safe_float(row.get('市净率', 0)),
                            'ps_ttm': self._safe_float(row.get('市销率', 0)),
                            'total_market_cap': self._safe_float(row.get('总市值', 0)) * 100000000,
                            'float_market_cap': self._safe_float(row.get('流通市值', 0)) * 100000000,
                            'roe': self._safe_float(row.get('净资产收益率 - 加权', 0)),
                            'eps': self._safe_float(row.get('每股收益', 0)),
                            'bvps': self._safe_float(row.get('每股净资产', 0)),
                            'dividend_yield': self._safe_float(row.get('股息率', 0))
                        }
                        
            except Exception as e:
                if attempt < retry - 1:
                    logger.warning(f"基本面数据尝试 {attempt+1}/{retry} 失败：{e}")
                    time.sleep(2)
                else:
                    logger.error(f"基本面数据获取失败 {stock_code}: {e}")
        
        # 备用方案：返回模拟数据
        logger.warning(f"使用模拟基本面数据：{stock_code}")
        return self._generate_mock_fundamental(stock_code)
    
    def _generate_mock_fundamental(self, stock_code: str) -> Dict:
        """生成模拟基本面数据"""
        np.random.seed(int(stock_code) % 1000 + 100)
        return {
            'stock_code': stock_code,
            'name': f'股票{stock_code}',
            'pe_ttm': 10 + np.random.rand() * 20,
            'pb': 1 + np.random.rand() * 3,
            'ps_ttm': 2 + np.random.rand() * 5,
            'total_market_cap': (100 + np.random.rand() * 900) * 100000000,
            'float_market_cap': (50 + np.random.rand() * 400) * 100000000,
            'roe': 5 + np.random.rand() * 20,
            'eps': 0.5 + np.random.rand() * 2,
            'bvps': 5 + np.random.rand() * 10,
            'dividend_yield': 1 + np.random.rand() * 3
        }
    
    def fetch_financial_data(self, stock_code: str) -> Optional[Dict]:
        """获取财务指标数据"""
        if not HAS_AK:
            return None
        
        try:
            # 获取财务指标
            df = ak.stock_financial_analysis_indicator(symbol=stock_code)
            
            if df is None or df.empty:
                return None
            
            # 取最新一期
            latest = df.iloc[0] if len(df) > 0 else None
            
            if latest is None:
                return None
            
            return {
                'revenue_growth': self._safe_float(latest.get('营业收入增长率', 0)),
                'profit_growth': self._safe_float(latest.get('净利润增长率', 0)),
                'debt_ratio': self._safe_float(latest.get('资产负债率', 0)),
                'gross_margin': self._safe_float(latest.get('销售毛利率', 0)),
                'net_margin': self._safe_float(latest.get('销售净利率', 0)),
                'roe': self._safe_float(latest.get('净资产收益率', 0))
            }
            
        except Exception as e:
            logger.error(f"获取财务数据失败 {stock_code}: {e}")
            return None
    
    def _safe_float(self, value) -> float:
        """安全转换为浮点数"""
        try:
            if value is None or value == '' or value == '-':
                return 0.0
            return float(value)
        except:
            return 0.0
    
    def analyze(self, stock_code: str, market: str = "") -> Dict:
        """综合基本面分析"""
        # 获取实时基本面数据
        basic_data = self.fetch_fundamental_data(stock_code)
        
        # 获取财务指标
        financial_data = self.fetch_financial_data(stock_code)
        
        if not basic_data:
            return {'error': '获取数据失败'}
        
        # 合并数据
        data = {**basic_data, **(financial_data or {})}
        
        # 估值评分
        valuation_score = self._evaluate_valuation(data)
        
        # 成长性评分
        growth_score = self._evaluate_growth(data)
        
        # 财务健康评分
        health_score = self._evaluate_health(data)
        
        # 综合评分
        total_score = (valuation_score + growth_score + health_score) / 3
        
        return {
            'stock_code': stock_code,
            'name': data.get('name', ''),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metrics': {
                'PE': round(data['pe_ttm'], 2),
                'PB': round(data['pb'], 2),
                'ROE': round(data.get('roe', 0), 2),
                'debt_ratio': round(data.get('debt_ratio', 0), 2),
                'revenue_growth': round(data.get('revenue_growth', 0), 2),
                'profit_growth': round(data.get('profit_growth', 0), 2),
                'gross_margin': round(data.get('gross_margin', 0), 2),
                'net_margin': round(data.get('net_margin', 0), 2)
            },
            'scores': {
                'valuation': valuation_score,
                'growth': growth_score,
                'health': health_score,
                'total': round(total_score, 1)
            },
            'evaluation': self._generate_evaluation(total_score, valuation_score, growth_score, health_score)
        }
    
    def _evaluate_valuation(self, data: Dict) -> float:
        """估值评分 (0-100)"""
        score = 50
        
        pe = data.get('pe_ttm', 0)
        if 0 < pe < 10:
            score += 30
        elif 10 <= pe < 20:
            score += 20
        elif 20 <= pe < 30:
            score += 10
        elif pe > 50:
            score -= 20
        
        pb = data.get('pb', 0)
        if 0 < pb < 1:
            score += 20
        elif 1 <= pb < 3:
            score += 10
        elif pb > 5:
            score -= 10
        
        return max(0, min(100, score))
    
    def _evaluate_growth(self, data: Dict) -> float:
        """成长性评分 (0-100)"""
        score = 50
        
        rev_growth = data.get('revenue_growth', 0)
        if rev_growth > 30:
            score += 30
        elif rev_growth > 15:
            score += 20
        elif rev_growth > 5:
            score += 10
        elif rev_growth < -10:
            score -= 20
        
        profit_growth = data.get('profit_growth', 0)
        if profit_growth > 30:
            score += 30
        elif profit_growth > 15:
            score += 20
        elif profit_growth > 5:
            score += 10
        elif profit_growth < -10:
            score -= 20
        
        return max(0, min(100, score))
    
    def _evaluate_health(self, data: Dict) -> float:
        """财务健康评分 (0-100)"""
        score = 50
        
        roe = data.get('roe', 0)
        if roe > 20:
            score += 25
        elif roe > 15:
            score += 20
        elif roe > 10:
            score += 10
        elif roe < 0:
            score -= 20
        
        debt_ratio = data.get('debt_ratio', 0)
        if debt_ratio < 30:
            score += 20
        elif debt_ratio < 50:
            score += 10
        elif debt_ratio > 70:
            score -= 20
        
        gross_margin = data.get('gross_margin', 0)
        if gross_margin > 40:
            score += 15
        elif gross_margin > 20:
            score += 10
        elif gross_margin < 10:
            score -= 10
        
        return max(0, min(100, score))
    
    def _generate_evaluation(self, total: float, valuation: float, 
                            growth: float, health: float) -> str:
        """生成评价"""
        if total >= 80:
            return "优秀 - 基本面强劲，值得长期关注"
        elif total >= 60:
            return "良好 - 基本面较好，可适当配置"
        elif total >= 40:
            return "一般 - 基本面平平，需谨慎观察"
        else:
            return "较差 - 基本面存在风险，建议规避"


class StockAnalyzer:
    """股票分析主类"""
    
    def __init__(self, config_path: str = 'config.json'):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {}
        
        self.tech_analyzer = TechnicalAnalyzer()
        self.fund_analyzer = FundamentalAnalyzer()
    
    def analyze_stock(self, stock: Dict) -> Dict:
        """分析单只股票"""
        code = stock['code']
        market = stock.get('market', '')
        name = stock.get('name', '')
        
        result = {
            'stock_code': code,
            'name': name,
            'market': market,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 技术分析
        if self.config.get('analysis', {}).get('technical', {}).get('enabled', True):
            result['technical'] = self.tech_analyzer.analyze(code, market)
        
        # 基本面分析
        if self.config.get('analysis', {}).get('fundamental', {}).get('enabled', True):
            result['fundamental'] = self.fund_analyzer.analyze(code, market)
        
        # 综合评级
        result['rating'] = self._calculate_rating(result)
        
        return result
    
    def analyze_all(self) -> List[Dict]:
        """分析所有配置的股票"""
        results = []
        
        for stock in self.config.get('stocks', []):
            logger.info(f"分析 {stock.get('name', stock['code'])} ({stock['code']})...")
            result = self.analyze_stock(stock)
            results.append(result)
            time.sleep(1)  # 避免请求过快
        
        return results
    
    def _calculate_rating(self, result: Dict) -> Dict:
        """计算综合评级"""
        tech_signals = result.get('technical', {}).get('signals', [])
        fund_score = result.get('fundamental', {}).get('scores', {}).get('total', 50)
        
        # 技术信号评分
        tech_score = 50
        buy_signals = sum(1 for s in tech_signals if s.get('signal') == '买入')
        sell_signals = sum(1 for s in tech_signals if s.get('signal') == '卖出')
        
        tech_score += (buy_signals - sell_signals) * 15
        
        # 趋势加分
        trend = result.get('technical', {}).get('trend', '')
        if trend == '上升趋势':
            tech_score += 15
        elif trend == '下降趋势':
            tech_score -= 15
        
        # 综合评分
        total_score = (tech_score + fund_score) / 2
        
        if total_score >= 80:
            rating = '强烈推荐'
        elif total_score >= 65:
            rating = '推荐'
        elif total_score >= 50:
            rating = '中性'
        elif total_score >= 35:
            rating = '谨慎'
        else:
            rating = '回避'
        
        return {
            'score': round(total_score, 1),
            'rating': rating,
            'tech_score': round(tech_score, 1),
            'fund_score': round(fund_score, 1)
        }


if __name__ == '__main__':
    # 测试
    if not HAS_AK:
        print("请先安装 akshare: pip install akshare")
    else:
        analyzer = StockAnalyzer()
        results = analyzer.analyze_all()
        
        for r in results:
            print(f"\n{r.get('name', '')} ({r['stock_code']})")
            print(f"  评级：{r['rating']['rating']} ({r['rating']['score']}分)")
            if 'technical' in r:
                print(f"  技术信号：{len(r['technical'].get('signals', []))} 个")
            if 'fundamental' in r:
                print(f"  基本面评分：{r['fundamental'].get('scores', {}).get('total', 0)}分")
