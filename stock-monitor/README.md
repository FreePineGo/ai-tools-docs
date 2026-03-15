# 股票监控脚本 📈

A 股股票实时监控工具，支持价格提醒、涨跌幅统计、自动导出。

## 功能

✅ 实时行情监控（东方财富接口）
✅ 价格波动提醒
✅ 涨跌幅统计
✅ 自动刷新
✅ 导出 Excel/CSV
✅ 支持多股票同时监控

## 快速开始

```bash
# 安装依赖
pip install requests pandas openpyxl

# 运行监控
python monitor.py

# 或者指定股票
python monitor.py 601857 600028 600938
```

## 配置文件

编辑 `config.json` 设置：
- 监控股票列表
- 价格提醒阈值
- 刷新频率

## 输出

- 终端实时显示行情
- 日志文件 `logs/monitor.log`
- 数据导出 `data/stock_data.csv`
