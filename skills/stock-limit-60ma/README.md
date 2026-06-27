# 涨停上穿60MA选股

筛选当日涨停且股价上穿 60 日均线的 A 股标的，用于短线选股、打板策略和技术面突破识别。

## 快速开始

```bash
pip install akshare pandas
python scripts/filter_limit_60ma.py --date 2026-03-31 --output json
```

## 核心逻辑

- **涨停**：当日达到涨停板
- **上穿60MA**：当日收盘价 > 60日均线，且前一日收盘价 <= 60日均线

当两个条件同时满足时，视为技术面强势突破信号。

## 使用方式

```bash
# 默认查询最近交易日
python scripts/filter_limit_60ma.py

# 指定日期
python scripts/filter_limit_60ma.py --date 2026-03-31

# 输出为 CSV
python scripts/filter_limit_60ma.py --output csv

# 保存到文件
python scripts/filter_limit_60ma.py --date 2026-03-31 --output json --output-file result.json
```

## 输出字段

| 字段 | 说明 |
|------|------|
| 代码 | 股票代码 |
| 名称 | 股票名称 |
| 收盘价 | 当日收盘价 |
| 涨停价 | 涨停板价格 |
| 连板数 | 连续涨停天数 |
| 首次封板时间 | 当日首次封板时间 |
| 最后封板时间 | 当日最后封板时间 |

## 数据来源

- 涨停数据：AKShare `stock_zt_pool_em`（东方财富涨停池）
- 历史行情：AKShare `stock_zh_a_hist`（A股历史行情）

## 依赖

- Python >= 3.9
- akshare >= 1.11.0
- pandas >= 1.5.0

## 注意事项

- 涨停池数据通常在交易日 16:00 后完整，建议盘后运行
- 停牌和新股（上市不足 65 天）会自动跳过
- 依赖网络连接获取实时数据

## WorkBuddy Skill

此项目为 WorkBuddy 技能包，安装后直接对 AI 说"涨停选股"或"筛选上穿60MA的涨停股"即可调用。
