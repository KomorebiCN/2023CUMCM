# %%
import pmdarima as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

df = pd.read_excel("附件3.xlsx")
df

# %%
df2 = pd.read_excel("数据清洗后.xlsx")
df2

# %%
new_dict = {}
for code,items in zip(df2["单品编码"].unique(),df2["单品名称"].unique()):
    new_dict[code]=items
new_dict
# 使用 .map() 方法将编码映射为名字并添加为新列
df['单品名称'] = df['单品编码'].map(new_dict)
df.dropna(inplace=True)
df.reset_index(drop=True,inplace=True)

# %%
data = {'Date': ['2023-07-01', '2023-07-02', '2023-07-03', '2023-07-04', '2023-07-05', '2023-07-06','2023-07-07']}

df_forcast = pd.DataFrame(data,columns=["Date"])

# %%
grouped=df.groupby("单品名称")
fig, ax = plt.subplots(figsize=(10, 6), dpi=300,facecolor='white')
#for name in grouped["单品名称"].unique():
#    group_A = grouped.get_group(name)
#    fig, ax = plt.subplots(figsize=(10, 6), dpi=300,facecolor='white')
#    plt.rcParams['font.sans-serif'] = ['SimHei']
#    plt.rcParams['axes.unicode_minus'] = False
#    ax.plot(grouped['Date'].loc[name], grouped[name].loc["批发价"], label=name)
#    ax.legend(loc='upper right')
#    ax.tick_params(axis='x', rotation=90)
#    plt.tight_layout()  # 自动调整布局以防止标签被裁剪
#    plt.savefig("outPNG2/{}.png".format(name), dpi=300)  # 保存图像为文件（可选）
#    plt.close()
for name, group_data in grouped:
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300, facecolor='white')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    ax.plot(group_data['日期'], group_data['批发价格(元/千克)'], label=name)
    ax.legend(loc='upper right')
    ax.tick_params(axis='x', rotation=90)
    plt.xlabel("日期")
    plt.ylabel("批发价格(元/千克)")
    plt.tight_layout()  # 自动调整布局以防止标签被裁剪
    plt.savefig("outPNG2/{}.png".format(name), dpi=300)  # 保存图像为文件（可选）
    plt.close()

# %%
data = {'Date': ['2023-07-01', '2023-07-02', '2023-07-03', '2023-07-04', '2023-07-05', '2023-07-06','2023-07-07']}

df_forcast = pd.DataFrame(data,columns=["Date"])

# %%

num_periods = 7

for name, group_data in grouped:
    time_series_data = group_data['批发价格(元/千克)']
# 自动选择最佳ARIMA模型
    model = pm.auto_arima(time_series_data, seasonal=False)

# 预测未来值
    forecast = model.predict(n_periods=num_periods)
    df_forcast[name]=forecast.tolist()

# %%
df_forcast.to_excel("批发价预测.xlsx",index=False)

# %%



