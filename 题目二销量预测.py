# %%
import pmdarima as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

df = pd.read_excel("日销量.xlsx")

# %%
df.set_index('Date', inplace=True)
df

# %%
data = {'Date': ['2023-07-01', '2023-07-02', '2023-07-03', '2023-07-04', '2023-07-05', '2023-07-06','2023-07-07']}

df_forcast = pd.DataFrame(data,columns=["Date"])
# 将"Date"列转换为日期时间类型
#df_forcast['Date'] = pd.to_datetime(df_forcast['Date'])

# 将"Date"列设置为索引
#df_forcast.set_index('Date', inplace=True)



df_forcast

# %%
num_periods = 7

for i in range(df.shape[1]):
    time_series_data = df.iloc[:,i]
# 自动选择最佳ARIMA模型
    model = pm.auto_arima(time_series_data, seasonal=False)

# 预测未来值
    forecast = model.predict(n_periods=num_periods)
    df_forcast[df.columns[i]]=forecast.tolist()
    

# %%
df_forcast.to_excel("销量预测.xlsx",index=0)

# %%



