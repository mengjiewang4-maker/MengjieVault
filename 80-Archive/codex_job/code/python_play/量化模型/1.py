import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def run_china_momentum_backtest(symbol="sh000300", short_win=20, long_win=60):
    """
    国内指数动量策略回测完整模板
    :param symbol: 指数代码，如 sh000300 (沪深300), sh000001 (上证指数)
    :param short_win: 短周期均线 (快线)
    :param long_win: 长周期均线 (慢线)
    """
    
    # 1. 解决 Mac 中文乱码问题
    # 尝试设置 Mac 自带的中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC']
    plt.rcParams['axes.unicode_minus'] = False 
    
    # 2. 获取数据
    print(f"正在从 AkShare 获取 {symbol} 历史数据...")
    try:
        df_raw = ak.stock_zh_index_daily(symbol=symbol)
    except Exception as e:
        return f"获取数据失败: {e}"

    # 3. 数据预处理
    df = df_raw[['date', 'close']].copy()
    df['date'] = pd.to_datetime(df['date'])
    # 重要：确保时间轴是从旧到新排序
    df = df.sort_values('date').reset_index(drop=True)
    # 确保数值类型正确
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    # 4. 计算策略指标
    df['MA_Fast'] = df['close'].rolling(window=short_win).mean()
    df['MA_Slow'] = df['close'].rolling(window=long_win).mean()

    # 5. 生成交易信号 (1为持仓, 0为清仓)
    # 只有当快线 > 慢线时才买入
    df['Signal'] = 0.0
    # 从有数据的地方开始计算，避免 NaN 干扰
    df.loc[long_win:, 'Signal'] = np.where(
        df['MA_Fast'][long_win:] > df['MA_Slow'][long_win:], 1.0, 0.0
    )

    # 6. 计算收益率 (核心回测逻辑)
    # 市场每日涨跌幅
    df['Market_Ret'] = df['close'].pct_change()
    # 策略每日收益：昨天的信号 * 今天的市场涨跌幅 (避免未来函数)
    df['Strategy_Ret'] = df['Signal'].shift(1) * df['Market_Ret']

    # 7. 计算累计净值 (假设初始资金为 1)
    df['Cum_Market'] = (1 + df['Market_Ret'].fillna(0)).cumprod()
    df['Cum_Strategy'] = (1 + df['Strategy_Ret'].fillna(0)).cumprod()

    # 8. 打印最后几行数据用于调试
    print("\n--- 回测数据预览 (最后5行) ---")
    print(df[['date', 'close', 'MA_Fast', 'MA_Slow', 'Signal', 'Cum_Strategy']].tail())

    # 9. 绘图可视化
    plt.figure(figsize=(12, 7), dpi=100)
    plt.plot(df['date'], df['Cum_Market'], label=f'基准指数 ({symbol})', color='gray', alpha=0.4, lw=1.5)
    plt.plot(df['date'], df['Cum_Strategy'], label='动量策略 (双均线)', color='#d62728', lw=2)
    
    # 装饰图表
    plt.title(f'量化策略回测: {symbol} 动量模型', fontsize=15)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('累计净值 (初始为1)', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # 填充持仓区间 (可选：直观查看什么时候在仓位里)
    plt.fill_between(df['date'], df['Cum_Strategy'].min(), df['Cum_Strategy'].max(), 
                     where=(df['Signal']==1), color='green', alpha=0.05, label='持仓区间')
    
    plt.tight_layout()
    plt.show()

    # 10. 输出简单的业绩指标
    total_return = (df['Cum_Strategy'].iloc[-1] - 1) * 100
    ann_return = ((df['Cum_Strategy'].iloc[-1])**(252/len(df)) - 1) * 100
    print(f"\n--- 策略评价 ---")
    print(f"测试时间范围: {df['date'].iloc[0].date()} 至 {df['date'].iloc[-1].date()}")
    print(f"策略总收益率: {total_return:.2f}%")
    print(f"年化收益率: {ann_return:.2f}%")

if __name__ == "__main__":
    # 你可以尝试修改 symbol 为 'sh000001' (上证) 或 'sz399006' (创业板)
    run_china_momentum_backtest(symbol="sh000300")