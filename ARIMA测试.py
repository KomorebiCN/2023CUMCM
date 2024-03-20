# %%
import pmdarima as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

df = pd.read_excel("日销量.xlsx")
df.set_index('Date', inplace=True)
df

# %%
df_example = df.loc[:,["西兰花"]]
df_example

# %%
df_test = df_example.copy()

# %%
df_test.iloc[range(df_test.shape[0]-31,df_test.shape[0]),0]=0
df_test

# %%
import matplotlib.pyplot as plt
import pmdarima as pm

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 原始数据
R = range(df_test.shape[0]-30, df_test.shape[0])
original_data = df_example.iloc[R, 0]

# 创建一个画布
plt.figure(figsize=(10, 6), dpi=300)

# 绘制原始数据
plt.plot(df_example.index[R], original_data, label="原始数据")

# 绘制其他三幅图像
model_periods =  [30]
for period in model_periods:
    df_test_copy = df_test.copy()
    for i in range(df_test_copy.shape[0]-30, df_test_copy.shape[0]):
        time_series_data = df_example.iloc[range(i-period, i), 0]
        model = pm.auto_arima(time_series_data, seasonal=False)
        df_test_copy.iloc[i, 0] = model.predict(n_periods=1)
    plt.plot(df_test.index[R], df_test_copy.iloc[R, 0], label=f"参数设置{period}天")

# 添加图例
plt.legend(loc='upper right', fontsize=10)


# %%


# %%



