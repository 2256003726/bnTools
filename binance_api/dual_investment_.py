#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：bnTools 
@File    ：dual_investment_.py 双币投资
@Author  ：王金鹏
@Date    ：2025/1/17 16:31
"""
from binance.client import Client

# 输入你的 API key 和 Secret key
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# 创建客户端
client = Client(api_key, api_secret)

# 获取双币策略产品的最新行情信息
def get_dual_investment_info():
    # 获取币安的双币策略市场的报价
    # 币安并没有专门的API接口获取Dual Investment策略的APR，所以我们可以通过现有的交易对信息来估算。
    # 比如获取 BTC/USDT 当前价格：
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    print(f"BTC/USDT 当前价格: {ticker['price']}")

    # 获取其他必要的信息，比如APR等可能需要通过币安官网或其他接口来查询
    # 币安的双币策略可能不直接提供通过API获取APR，你可能需要查看官网的相应页面，或者获取相关产品的API。

# 执行获取信息
get_dual_investment_info()
