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

# Define price range and strategies
prices = list(range(98000, 100001, 500))
strategies = {
    "99000 (APR 206%)": 206 / 365 / 100,
    "98500 (APR 160%)": 160 / 365 / 100,
    "98000 (APR 103%)": 103 / 365 / 100,
}
principal = 10000  # Principal amount in USDT

# Calculate daily returns and potential outcomes for each strategy
data = []
for price in prices:
    row = {"Price (USDT)": price}
    for strategy, apr in strategies.items():
        target_price = int(strategy.split()[0])
        daily_yield = principal * apr
        if price >= target_price:
            # If price >= target_price, return principal + interest
            return_rate = ((principal + daily_yield) / principal - 1) * 100
            row[strategy] = return_rate
        else:
            # If price < target_price, calculate BTC amount bought and its market value
            btc_bought = principal / target_price
            return_rate = ((btc_bought * price + daily_yield) / principal - 1) * 100
            row[strategy] = return_rate  # Market value of BTC bought
    data.append(row)

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