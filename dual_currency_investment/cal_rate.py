import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def calculate_daily_yield(principal, apr, hours):
    """
    计算每日收益

    :param principal: 本金 (单位: USDT)
    :param apr: 年利率（APR），格式为小数 (例如：206% -> 206/365/100)
    :param days: 收益计算的小时数

    :return: 返回根据年利率和天数计算的每日收益
    """
    return principal * apr * hours


def calculate_return_rate(principal, price, target_price, daily_yield):
    """
    根据实际价格和目标价格计算收益率

    :param principal: 本金 (单位: USDT)
    :param price: 当前实际价格 (单位: USDT)
    :param target_price: 目标价格
    :param daily_yield: 根据策略计算出的每日收益

    :return: 当前实际价格下的收益率，单位百分比
    """
    if price >= target_price:
        # 当实际价格大于或等于目标价格时，按目标价格计算收益
        return_rate = ((principal + daily_yield) / principal - 1) * 100
    else:
        # 当实际价格小于目标价格时，按实际价格计算收益
        btc_bought = principal / target_price  # 买入的比特币数量
        return_rate = ((btc_bought * price + daily_yield) / principal - 1) * 100

    return round(return_rate, 3)  # 保留三位小数


def calculate_investment_returns(prices, strategies, principal, hours):
    """
    计算每种策略下的收益率

    :param prices: 实际市场价格的列表 (单位: USDT)
    :param strategies: 投资策略字典，包含每个策略的目标价格和APR
    :param principal: 本金 (单位: USDT)
    :param days: 收益计算的天数

    :return: 返回一个包含收益率的 DataFrame，行表示价格，列表示不同策略的收益率
    """
    data = {"Price (USDT)": prices}

    # 计算每日收益率
    daily_yields = {strategy: calculate_daily_yield(principal, apr, hours) for strategy, apr in strategies.items()}

    for strategy, apr in strategies.items():
        target_price = float(strategy.split()[0])  # 提取目标价格（例如 "99000"）
        daily_yield = daily_yields[strategy]
        returns = []

        # 遍历不同价格，计算收益率
        for price in prices:
            return_rate = calculate_return_rate(principal, price, target_price, daily_yield)
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
    # 设定目标价格范围 和 双币投资策略
    prices = np.arange(0.9, 1.1, 0.001)  # 生成价格范围：从 0.9 到 1.01，步长为 0.01
    strategies = {
        "0.95 (APR 206%)": 206 / 365 / 24 / 100,
        "0.98 (APR 160%)": 160 / 365 / 24 / 100,
        "0.97 (APR 103%)": 103 / 365 / 24 / 100,
    }
    principal = 1  # 初始本金
    hours = 24 * 4  # 控制收益天数的变量

    # 计算收益率
    df = calculate_investment_returns(prices, strategies, principal, hours)
    print(df)

    # 绘制结果图
    plot_results(df, strategies)


if __name__ == "__main__":
    main()
