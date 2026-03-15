#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股股票监控脚本
实时监控股票价格、涨跌幅、成交量等数据
"""

import requests
import pandas as pd
import json
import time
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

# 配置日志
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/monitor_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StockMonitor:
    """股票监控器"""
    
    # 东方财富实时行情接口
    API_URL = "http://push2.eastmoney.com/api/qt/stock/get"
    
    def __init__(self, config_path: str = 'config.json'):
        """初始化监控器"""
        self.config = self.load_config(config_path)
        self.stocks = self.config.get('stocks', [])
        self.alert_config = self.config.get('alert', {})
        self.refresh_interval = self.config.get('refresh_interval', 5)
        
        # 存储历史数据
        self.history_data: List[Dict] = []
        self.last_prices: Dict[str, float] = {}
        
        logger.info(f"股票监控器已启动，监控 {len(self.stocks)} 只股票")
    
    def load_config(self, path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {path} 不存在，使用默认配置")
            return self.default_config()
    
    def default_config(self) -> Dict:
        """默认配置"""
        return {
            "stocks": [
                {"code": "601857", "name": "中国石油", "market": "SH"},
                {"code": "600028", "name": "中国石化", "market": "SH"},
                {"code": "600938", "name": "中国海油", "market": "SH"}
            ],
            "alert": {"price_change_threshold": 3.0},
            "refresh_interval": 5
        }
    
    def get_stock_code(self, stock: Dict) -> str:
        """生成东方财富股票代码格式"""
        market = stock.get('market', 'SH')
        code = stock.get('code', '')
        return f"{market}.{code}"
    
    def fetch_stock_data(self, stock: Dict) -> Optional[Dict]:
        """获取单只股票实时数据"""
        try:
            params = {
                'secid': self.get_stock_code(stock),
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100'
            }
            
            response = requests.get(self.API_URL, params=params, timeout=5)
            data = response.json()
            
            if data.get('data'):
                stock_data = data['data']
                return {
                    'code': stock['code'],
                    'name': stock['name'],
                    'price': stock_data.get('f43', 0) / 100,  # 当前价
                    'open': stock_data.get('f46', 0) / 100,   # 开盘价
                    'high': stock_data.get('f44', 0) / 100,   # 最高价
                    'low': stock_data.get('f45', 0) / 100,    # 最低价
                    'prev_close': stock_data.get('f60', 0) / 100,  # 昨收
                    'change': stock_data.get('f170', 0) / 100,     # 涨跌额
                    'change_pct': stock_data.get('f171', 0) / 100, # 涨跌幅%
                    'volume': stock_data.get('f47', 0),            # 成交量
                    'amount': stock_data.get('f48', 0),            # 成交额
                    'turnover': stock_data.get('f168', 0),         # 换手率%
                    'pe': stock_data.get('f162', 0),               # 市盈率
                    'pb': stock_data.get('f167', 0),               # 市净率
                    'total_market_cap': stock_data.get('f116', 0), # 总市值
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            logger.error(f"获取 {stock['name']} 数据失败：{e}")
        
        return None
    
    def check_alert(self, stock_data: Dict) -> List[str]:
        """检查是否触发提醒"""
        alerts = []
        threshold = self.alert_config.get('price_change_threshold', 3.0)
        
        code = stock_data['code']
        current_price = stock_data['price']
        change_pct = abs(stock_data['change_pct'])
        
        # 价格涨跌幅提醒
        if change_pct >= threshold:
            direction = "📈" if stock_data['change_pct'] > 0 else "📉"
            alerts.append(
                f"{direction} {stock_data['name']} ({code}) "
                f"涨跌幅超阈值：{stock_data['change_pct']:+.2f}%"
            )
        
        # 价格大幅波动提醒
        if code in self.last_prices:
            price_change = abs(current_price - self.last_prices[code])
            if price_change > 0.5:  # 单次刷新波动超过 0.5 元
                alerts.append(
                    f"⚠️ {stock_data['name']} ({code}) "
                    f"价格大幅波动：¥{price_change:.2f}"
                )
        
        # 更新最后价格
        self.last_prices[code] = current_price
        
        return alerts
    
    def display_stock_data(self, stock_data: Dict):
        """格式化显示股票数据"""
        change_color = "🟢" if stock_data['change_pct'] > 0 else "🔴" if stock_data['change_pct'] < 0 else "⚪"
        
        print(f"\n{change_color} {stock_data['name']} ({stock_data['code']})")
        print(f"   当前价：¥{stock_data['price']:.2f}")
        print(f"   涨跌：{stock_data['change']:+.2f} ({stock_data['change_pct']:+.2f}%)")
        print(f"   开盘：¥{stock_data['open']:.2f} | 最高：¥{stock_data['high']:.2f} | 最低：¥{stock_data['low']:.2f}")
        print(f"   昨收：¥{stock_data['prev_close']:.2f}")
        print(f"   成交量：{stock_data['volume']/10000:.1f}万手 | 成交额：{stock_data['amount']/100000000:.1f}亿")
        print(f"   换手：{stock_data['turnover']:.2f}% | 市盈：{stock_data['pe']:.2f} | 市净：{stock_data['pb']:.2f}")
        print(f"   总市值：{stock_data['total_market_cap']/100000000:.1f}亿")
        print(f"   时间：{stock_data['timestamp']}")
    
    def export_to_csv(self, data: List[Dict]):
        """导出数据到 CSV"""
        if not data:
            return
        
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(data)
        
        # 按股票代码 + 日期保存
        today = datetime.now().strftime('%Y%m%d')
        filename = f'data/stock_data_{today}.csv'
        
        # 追加模式
        if os.path.exists(filename):
            existing_df = pd.read_csv(filename, encoding='utf-8')
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"数据已导出到 {filename}")
    
    def monitor_once(self) -> List[Dict]:
        """执行一次监控"""
        results = []
        
        for stock in self.stocks:
            stock_data = self.fetch_stock_data(stock)
            
            if stock_data:
                results.append(stock_data)
                self.display_stock_data(stock_data)
                
                # 检查提醒
                alerts = self.check_alert(stock_data)
                for alert in alerts:
                    logger.warning(alert)
                    print(f"   {alert}")
            
            time.sleep(0.5)  # 避免请求过快
        
        return results
    
    def run(self, duration: Optional[int] = None):
        """
        运行监控
        
        Args:
            duration: 监控时长（秒），None 表示持续运行
        """
        logger.info("开始监控...")
        print("\n" + "="*60)
        print("📊 A 股股票监控器".center(60))
        print("="*60)
        
        start_time = time.time()
        export_timer = 0
        
        try:
            while True:
                # 执行一次监控
                stock_data = self.monitor_once()
                self.history_data.extend(stock_data)
                
                # 导出检查
                export_timer += self.refresh_interval
                if self.config.get('export', {}).get('enabled', True):
                    if export_timer >= self.config.get('export', {}).get('interval_minutes', 30) * 60:
                        self.export_to_csv(stock_data)
                        export_timer = 0
                
                # 时长检查
                if duration and (time.time() - start_time) >= duration:
                    logger.info(f"监控时长已达 {duration} 秒，停止监控")
                    break
                
                # 显示下次刷新
                print(f"\n⏱️  下次刷新：{self.refresh_interval} 秒后... (Ctrl+C 停止)")
                time.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            logger.info("用户中断监控")
            print("\n\n👋 监控已停止")
        except Exception as e:
            logger.error(f"监控异常：{e}")
            raise
        finally:
            # 最终导出
            if self.history_data:
                self.export_to_csv(self.history_data)
                logger.info(f"本次监控共记录 {len(self.history_data)} 条数据")
    
    def get_summary(self) -> Dict:
        """获取监控摘要"""
        if not self.history_data:
            return {}
        
        df = pd.DataFrame(self.history_data)
        
        summary = {}
        for code in df['code'].unique():
            stock_df = df[df['code'] == code]
            name = stock_df.iloc[0]['name']
            
            summary[code] = {
                'name': name,
                'avg_price': stock_df['price'].mean(),
                'max_price': stock_df['price'].max(),
                'min_price': stock_df['price'].min(),
                'current_price': stock_df.iloc[-1]['price'],
                'volatility': stock_df['price'].std(),
                'data_points': len(stock_df)
            }
        
        return summary


def main():
    """主函数"""
    import sys
    
    # 支持命令行指定股票代码
    monitor = StockMonitor()
    
    if len(sys.argv) > 1:
        # 从命令行读取股票代码
        codes = sys.argv[1:]
        monitor.stocks = [
            {"code": code, "name": f"股票{code}", "market": "SH" if code.startswith('6') else "SZ"}
            for code in codes
        ]
        logger.info(f"监控命令行指定的股票：{codes}")
    
    # 运行监控（默认持续运行）
    monitor.run()


if __name__ == '__main__':
    main()
