#!/usr/bin/env python3
"""
筛选当日涨停且股价上穿 60 日均线的股票

使用方法:
    python filter_limit_60ma.py [--date YYYY-MM-DD] [--output json|csv]

依赖:
    pip install akshare pandas
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import akshare as ak
    import pandas as pd
except ImportError as e:
    print(f"错误：缺少依赖库 - {e}", file=sys.stderr)
    print("请运行：pip install akshare pandas", file=sys.stderr)
    sys.exit(1)


def get_limit_up_stocks(date: str = None) -> pd.DataFrame:
    """
    获取指定日期的涨停股票列表
    
    Args:
        date: 日期字符串 YYYY-MM-DD，默认为最近交易日
        
    Returns:
        涨停股票 DataFrame
    """
    if date is None:
        # 获取最近交易日
        date = datetime.now().strftime("%Y%m%d")
    else:
        date = date.replace("-", "")
    
    try:
        # 获取涨停池数据
        df = ak.stock_zt_pool_em(date=date)
        return df
    except Exception as e:
        print(f"获取涨停数据失败：{e}", file=sys.stderr)
        return pd.DataFrame()


def check_cross_60ma(symbol: str, date: str = None) -> bool:
    """
    检查股票是否在指定日期上穿 60 日均线
    
    上穿条件：
    - 当日收盘价 > 60 日均线
    - 前一日收盘价 <= 前一日 60 日均线
    
    Args:
        symbol: 股票代码 (如：000001)
        date: 日期字符串 YYYY-MM-DD
        
    Returns:
        bool: 是否上穿 60MA
    """
    try:
        # 获取历史行情数据
        end_date = datetime.strptime(date.replace("-", ""), "%Y%m%d") if date else datetime.now()
        start_date = (end_date - timedelta(days=90)).strftime("%Y%m%d")
        end_date = end_date.strftime("%Y%m%d")
        
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                 start_date=start_date, end_date=end_date)
        
        if len(df) < 65:  # 需要至少 65 天数据来计算 60MA
            return False
        
        # 计算 60 日均线
        df['MA60'] = df['收盘'].rolling(window=60).mean()
        
        # 获取最新两天的数据
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 检查是否上穿：今日收盘>MA60 且 昨日收盘<=昨日 MA60
        cross_up = (latest['收盘'] > latest['MA60']) and (prev['收盘'] <= prev['MA60'])
        
        return cross_up
        
    except Exception as e:
        print(f"检查 {symbol} 的 60MA 失败：{e}", file=sys.stderr)
        return False


def filter_stocks(date: str = None, output_format: str = "json") -> list:
    """
    筛选涨停且上穿 60MA 的股票
    
    Args:
        date: 日期 YYYY-MM-DD
        output_format: 输出格式 json|csv
        
    Returns:
        符合条件的股票列表
    """
    print(f"正在获取 {date or '最近交易日'} 的涨停股票...", flush=True)
    
    # 获取涨停股票
    limit_df = get_limit_up_stocks(date)
    
    if limit_df.empty:
        print("未获取到涨停股票数据")
        return []
    
    print(f"找到 {len(limit_df)} 只涨停股票，开始筛选上穿 60MA 的标的...", flush=True)
    
    results = []
    total = len(limit_df)
    
    for idx, row in limit_df.iterrows():
        symbol = row.get('代码', row.get('股票代码', ''))
        name = row.get('名称', row.get('股票名称', ''))
        
        if not symbol:
            continue
            
        # 检查是否上穿 60MA
        if check_cross_60ma(symbol, date):
            result = {
                '代码': symbol,
                '名称': name,
                '收盘价': row.get('最新价', row.get('收盘价', 0)),
                '涨停价': row.get('涨停价', 0),
                '连板数': row.get('连板数', 0),
                '首次封板时间': row.get('首次封板时间', ''),
                '最后封板时间': row.get('最后封板时间', '')
            }
            results.append(result)
            print(f"  ✓ {symbol} {name} - 上穿 60MA")
        
        # 进度显示
        if (idx + 1) % 10 == 0:
            print(f"  进度：{idx + 1}/{total}", flush=True)
    
    print(f"\n筛选完成：{len(results)}/{total} 只股票符合条件")
    return results


def main():
    parser = argparse.ArgumentParser(description='筛选涨停且上穿 60MA 的股票')
    parser.add_argument('--date', type=str, help='日期 (YYYY-MM-DD)，默认为最近交易日')
    parser.add_argument('--output', type=str, choices=['json', 'csv'], default='json',
                        help='输出格式 (默认：json)')
    parser.add_argument('--output-file', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    results = filter_stocks(date=args.date, output_format=args.output)
    
    if not results:
        print("未找到符合条件的股票")
        return
    
    # 输出结果
    if args.output == 'json':
        output = json.dumps(results, indent=2, ensure_ascii=False)
    else:
        df = pd.DataFrame(results)
        output = df.to_csv(index=False, lineterminator='\n')
    
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n结果已保存到：{args.output_file}")
    else:
        print("\n" + "=" * 60)
        print(output)


if __name__ == "__main__":
    main()
