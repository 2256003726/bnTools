import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_daily_yield(btc_quantity, apr, hours):
    """
    计算每日收益

    :param btc_quantity: 本金 (单位: 比特币数量)
    :param apr: 年利率（APR），格式为小数 (例如：206% -> 206/365/100)
    :param hours: 收益计算的小时数

    :return: 返回根据年利率和小时数计算的每日收益
    """
    return btc_quantity * apr * hours  # 按小时数计算每日收益


def calculate_return_rate(btc_quantity, price, target_price, daily_yield):
    """
    根据实际价格和目标价格计算收益率

    :param btc_quantity: 持有BTC的数量 (单位: BTC)
    :param price: 当前市场价格 (单位: USDT)
    :param target_price: 目标价格
    :param daily_yield: 根据策略计算出的每日收益

    :return: 当前实际价格下的收益率，单位百分比
    """
    if price <= target_price:
        # 当实际价格小于目标价格时，继续持有BTC，收益=BTC数量*当前价格+每日收益-1
        return_rate = ((btc_quantity * price + daily_yield) - 1) * 100
    else:
        # 计算高卖时的收益，收益=以目标加卖出btc数量*目标价格+每日收益 - 如果不卖出的话此时btc数量*当前价格
        return_rate = ((target_price * btc_quantity + daily_yield) - price * btc_quantity) * 100

    return round(return_rate, 3)  # 保留三位小数


def calculate_investment_returns(prices, strategies, btc_quantity, hours):
    """
    计算每种策略下的收益率

    :param prices: 实际市场价格的列表 (单位: USDT)
    :param strategies: 投资策略字典，包含每个策略的目标价格和APR
    :param btc_quantity: 持有比特币的数量 (单位: 比特币)
    :param hours: 收益计算的小时数

    :return: 返回一个包含收益率的 DataFrame，行表示价格，列表示不同策略的收益率
    """
    data = {"Price (USDT)": prices}

    # 计算每日收益率
    daily_yields = {strategy: calculate_daily_yield(btc_quantity, apr, hours) for strategy, apr in strategies.items()}

    for strategy, apr in strategies.items():
        target_price = float(strategy.split()[0])  # 提取目标价格（例如 "1.05"）
        daily_yield = daily_yields[strategy]
        returns = []

        # 遍历不同价格，计算收益率
        for price in prices:
            return_rate = calculate_return_rate(btc_quantity, price, target_price, daily_yield)
            returns.append(return_rate)
        data[strategy] = returns

    return pd.DataFrame(data)


def plot_results(df, strategies):
    """
    绘制收益率的变化曲线图

    :param df: 包含策略和市场价格数据的 DataFrame
    :param strategies: 投资策略字典，用于图例标识
    """
    plt.figure(figsize=(10, 6))
    plt.rc("font", family='Microsoft YaHei')  # 设置中文字体

    # 设置收益率接近零的阈值
    threshold = 0.1  # 0.01% 认为是接近0的收益率

    for strategy in strategies.keys():
        plt.plot(df["Price (USDT)"], df[strategy], label=strategy)
        # 查找收益率接近0的点，并标出
        zero_return_price = df[(df[strategy] >= -threshold) & (df[strategy] <= threshold)]["Price (USDT)"]
        if not zero_return_price.empty:
            plt.scatter(zero_return_price, [0] * len(zero_return_price), color='red', zorder=5,
                        label=f"{strategy} - 接近0%收益")

    plt.title("收益率百分比变化 (Price vs. Strategy Percentage Return Rate)")
    plt.xlabel("Market Price (USDT)")
    plt.ylabel("收益率 (%)")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    # 设定目标价格范围 和 高卖投资策略
    prices = np.arange(0.9, 1.1, 0.001)  # 生成价格范围：从 0.9 到 1.1，步长为 0.001
    strategies = {
        "1.005 (APR 206%)": 206 / 365 / 24 / 100,
        "1.010 (APR 160%)": 130 / 365 / 24 / 100,
        "1.015 (APR 103%)": 100 / 365 / 24 / 100,
    }
    btc_quantity = 1  # 初始持有 1 BTC
    hours = 24  # 控制收益小时的变量

    # 计算收益率
    df = calculate_investment_returns(prices, strategies, btc_quantity, hours)
    print(df)

    # 绘制结果图
    plot_results(df, strategies)


if __name__ == "__main__":
    main()
