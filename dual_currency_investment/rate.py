#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：bnTools
@File    ：rate.py
@Author  ：王金鹏
@Date    ：2025/1/6 18:48
"""
import pandas as pd
import matplotlib.pyplot as plt

# 定义到期实际价格范围 和 双币投资策略
prices = list(range(98000, 100001, 500))
strategies = {
    "99000 (APR 206%)": 206 / 365 / 100,
    "98500 (APR 160%)": 160 / 365 / 100,
    "98000 (APR 103%)": 103 / 365 / 100,
}
principal = 10000  # Principal amount in USDT
days = 4  # 控制收益天数的变量

# 预计算每日收益率
daily_yields = {}
for strategy, apr in strategies.items():
    daily_yield = principal * apr * days  # 收益 = 本金 * 日利率 * 天数
    daily_yields[strategy] = daily_yield

# 计算每种策略的每日收益率和潜在结果
data = {"Price (USDT)": prices}
for strategy, apr in strategies.items():
    target_price = int(strategy.split()[0])
    daily_yield = daily_yields[strategy]
    returns = []
    for price in prices:
        if price >= target_price:
            return_rate = ((principal + daily_yield) / principal - 1) * 100
        else:
            btc_bought = principal / target_price  # 买入的比特币数量
            return_rate = ((btc_bought * price + daily_yield) / principal - 1) * 100
        returns.append(return_rate)
    data[strategy] = returns

# Create DataFrame
df = pd.DataFrame(data)
print(df)

# Plotting the results as line charts
plt.figure(figsize=(10, 6))
# 设置中文字体
plt.rc("font", family='Microsoft YaHei')
for strategy in strategies.keys():
    plt.plot(df["Price (USDT)"], df[strategy], label=strategy)

plt.title("收益率百分比变化 (Price vs. Strategy Percentage Return Rate)")
plt.xlabel("Market Price (USDT)")
plt.ylabel("收益率 (%)")
plt.legend()
plt.grid(True)
plt.show()