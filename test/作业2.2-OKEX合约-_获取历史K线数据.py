"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 第二章2.2作业目标：
每天实时收集OKEX交易所合约的K线数据；
永续+交割，币本位+USDT本位
交易对至少包含BTC
时间周期至少包含5min
通过获取历史K线数据，进一步讲解ccxt的用法
"""
from typing import Any, Union

import pandas as pd
import ccxt
import time
import os
from datetime import timedelta
from datetime import datetime
import dateutil.parser
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====设定参数
okex = ccxt.okex()
exchange = ccxt.okex()
# =====定义参数
params = {
    'instrument_id': 'BTC-USD-201225',
    'granularity': '300',
    'start': '2020-08-20T00:00:00.000Z',
    'end': '2020-08-21T00:00:00.000Z'
}
df = okex.futuresGetInstrumentsInstrumentIdCandles(params=params)

# =====抓取数据开始结束时间
start_time = '2020-08-21 00:00:00'
end_time = pd.to_datetime(start_time) + timedelta(days=1)
print("end_time=", end_time)

# =====开始循环抓取数据
df_list = []
start_time_since = exchange.parse8601(start_time)
while True:

    # 获取数据
    df = okex.futuresGetInstrumentsInstrumentIdCandles(params=params)
    # df = okex.swapGetInstrumentsInstrumentIdCandles(params=params)

    print("df1=", df)
    # 整理数据
    df = pd.DataFrame(df, dtype=float)  # 将数据转换为dataframe
    df['candle_begin_time'] = pd.to_datetime(df[0], unit='ns')  # 整理时间
    print("df2=", df)

    # 合并数据
    df_list.append(df)

    # 新的since
    t = pd.to_datetime(df.iloc[-1][0], unit='ns')
    print(t)

    start_time_since = exchange.parse8601(str(t))

    # 判断是否挑出循环
    # if t >= end_time or df.shape[0] <= 1:
    if t >= pd.to_datetime(end_time).tz_localize('Asia/Hong_Kong') or df.shape[0] <= 1:
        print('抓取完所需数据，或抓取至最新数据，完成抓取任务，退出循环')

    # 抓取间隔需要暂停1s，防止抓取过于频繁
    time.sleep(1)
    break

# =====合并整理数据
df = pd.concat(df_list, ignore_index=True)
df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                   3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名
df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ns')
df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]  # 整理列的顺序

# 选取数据时间段
df = df[df['candle_begin_time'].dt.date == pd.to_datetime(start_time).date()]

# 去重、排序
df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
df.sort_values('candle_begin_time', inplace=True)
df.reset_index(drop=True, inplace=True)

# =====保存数据到文件
if df.shape[0] > 0:
    # 根目录，确保该路径存在
    path = r'D:\douyin'

    # 创建交易所文件夹
    path = os.path.join(path, exchange.id)
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建futures文件夹
    path = os.path.join(path, 'futures')
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建日期文件夹
    path = os.path.join(path, str(pd.to_datetime(start_time).date()))
    if os.path.exists(path) is False:
        os.mkdir(path)

    # 拼接文件目录
    file_name = '_20200823.csv'
    path = os.path.join(path, file_name)
    print(path)

    df.to_csv(path, index=False)
    print(df)