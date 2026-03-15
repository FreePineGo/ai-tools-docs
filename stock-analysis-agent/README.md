# 股票分析 Agent 📊

完整的股票分析系统，基于 **AkShare** 数据接口，支持**技术分析**、**基本面分析**、**舆情监控**和**自动报告生成**。

## ✨ 功能特性

### 🔍 技术分析
- **K 线数据** - 实时获取日线/周线/月线数据（前复权）
- **均线系统** - MA5/10/20/60 自动计算
- **MACD** - 金叉/死叉信号识别
- **RSI** - 超买/超卖判断
- **KDJ** - 随机指标分析
- **布林带** - 波动区间判断
- **自动信号** - 买入/卖出/观望建议

### 📈 基本面分析
- **估值指标** - PE(TTM)、PB、PS
- **盈利能力** - ROE、毛利率、净利率
- **成长能力** - 营收增长率、利润增长率
- **财务健康** - 资产负债率
- **综合评分** - 0-100 分量化评估

### 📰 舆情监控
- **个股新闻** - 东方财富新闻抓取
- **公司公告** - 官方公告监控
- **情绪分析** - 正面/负面/中性判断
- **智能缓存** - 避免重复请求

### 📝 报告生成
- **日报** - 详细的 Markdown 格式报告
- **简报** - 快速查看的摘要版本
- **JSON 导出** - 便于程序调用
- **自动归档** - 按日期保存

## 🚀 快速开始

### 1. 安装依赖

```bash
cd stock-analysis-agent
pip install -r requirements.txt
```

### 2. 配置股票

编辑 `config.json`，添加你想分析的股票：

```json
{
  "stocks": [
    {"code": "601857", "name": "中国石油", "market": "SH"},
    {"code": "000858", "name": "五粮液", "market": "SZ"},
    {"code": "600519", "name": "贵州茅台", "market": "SH"}
  ]
}
```

### 3. 运行分析

```bash
# 分析所有配置的股票
python main.py

# 分析单只股票
python main.py -s 600519 -n 贵州茅台

# 输出 JSON 结果
python main.py --json

# 不使用缓存（获取最新舆情）
python main.py --no-cache
```

## 📂 目录结构

```
stock-analysis-agent/
├── main.py                 # 主入口
├── quick_analyzer.py       # 快速分析（独立脚本）
├── config.json             # 配置文件
├── requirements.txt        # 依赖
├── README.md              # 说明文档
├── src/
│   ├── analyzer.py        # 核心分析模块（AkShare）
│   ├── news_monitor.py    # 舆情监控（AkShare）
│   └── report_generator.py # 报告生成
├── reports/               # 报告输出目录
└── news_cache/            # 新闻缓存
```

## 📋 配置说明

### config.json

```json
{
  "stocks": [
    {"code": "600519", "name": "贵州茅台", "market": "SH"}
  ],
  "analysis": {
    "technical": {
      "enabled": true,
      "indicators": ["MA", "MACD", "RSI", "KDJ", "BOLL"]
    },
    "fundamental": {
      "enabled": true,
      "metrics": ["PE", "PB", "ROE", "debt_ratio"]
    },
    "sentiment": {
      "enabled": true,
      "cache_hours": 2
    }
  },
  "alerts": {
    "price_change_threshold": 3.0,
    "technical_signals": ["golden_cross", "death_cross"]
  },
  "report": {
    "auto_generate": true,
    "schedule": "daily"
  }
}
```

## 📊 输出示例

### 命令行输出

```
============================================================
              📊 股票分析 Agent (AkShare)                    
============================================================

🟢 贵州茅台 (600519)
   评级：强烈推荐 (85 分)
   趋势：上升趋势
   技术信号：2 个
     - MA5 上穿 MA10 金叉
     - RSI 超卖 (18.5)
   基本面：优秀 - 基本面强劲，值得长期关注 (88 分)
   舆情：😊 positive (0.75)
```

### 报告文件

- `reports/daily_report_2024-01-15.md` - 详细日报
- `reports/summary_2024-01-15.txt` - 简报
- `reports/analysis_result_2024-01-15.json` - JSON 数据

## 🔌 Python API 调用

```python
import sys
sys.path.insert(0, 'src')

from analyzer import StockAnalyzer
from news_monitor import NewsMonitor
from report_generator import ReportGenerator

# 初始化
analyzer = StockAnalyzer()
news_monitor = NewsMonitor()
report_gen = ReportGenerator()

# 分析单只股票
result = analyzer.analyze_stock({
    'code': '600519',
    'name': '贵州茅台'
})

print(f"评级：{result['rating']['rating']}")
print(f"评分：{result['rating']['score']}分")
print(f"趋势：{result['technical']['trend']}")

# 舆情监控
sentiment = news_monitor.monitor_stock('600519', '贵州茅台')
print(f"情绪：{sentiment['sentiment']['sentiment']}")

# 生成报告
report_path = report_gen.generate_daily_report([result], [sentiment])
```

## 🛠️ 常见问题

### 1. 安装 akshare 失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装 akshare
pip install akshare
```

### 2. 数据获取失败

- 检查网络连接
- 可能是接口限流，稍后重试
- 使用 `--no-cache` 强制刷新

### 3. 中文乱码

Windows 用户设置 UTF-8 编码：
```powershell
$env:PYTHONUTF8=1
```

## ⚠️ 免责声明

- 本工具仅供学习和研究使用
- 不构成任何投资建议
- 股市有风险，投资需谨慎
- 数据来源于 AkShare，可能存在延迟

## 📝 TODO

- [ ] 添加更多技术指标（威廉指标、CCI 等）
- [ ] 支持港股、美股
- [ ] 添加资金流向分析
- [ ] 支持自定义选股策略
- [ ] Web 界面
- [ ] 定时任务自动运行
- [ ] 微信/邮件推送

## 🔗 相关资源

- [AkShare 文档](https://akshare.akfamily.xyz/)
- [东方财富网](http://www.eastmoney.com/)

---

*Made with ❤️ by Stock Analysis Agent*
