# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

df1 = pd.read_excel("附件1.xlsx")
df1["单品编码"] = df1["单品编码"].astype(str)
df1["分类编码"] = df1["分类编码"].astype(str)
df2 = pd.read_excel("附件2.xlsx")
df2["单品编码"] = df2["单品编码"].astype(str)
df = pd.merge(df1,df2,on="单品编码")
df = df[df['销售类型'] != '退货']#删除退货的数据
df['扫码销售时间'] = pd.to_timedelta(df['扫码销售时间'])
df["销售时间"]= df["销售日期"]+df["扫码销售时间"]
df = df.sort_values(by="销售时间").reset_index(drop=True)

# %%
all_vegetables=pd.Series(df["单品编码"].unique())
all_kinds = pd.Series(df["分类编码"].unique())
all_vegetables.name = "单品编码"
all_kinds.name = "分类编码"

vegetables_sold = pd.DataFrame(columns=["单品编码","单品销售量"])
vegetables_sold["单品编码"]= all_vegetables
vegetables_sold["单品销售量"] = 0


# %%
def compute_sold(df,all,sold):
    for i in range(len(all)):
        sold.iloc[i,1]=df.loc[(df["单品编码"] == all[i]),["销量(千克)"]].sum()
    return sold
#计算单品销售量
vegetables_sold = compute_sold(df,all_vegetables,vegetables_sold)
vegetables_sold

# %%
vegetables_sold=vegetables_sold.sort_values(by="单品销售量",ascending=False).reset_index(drop=True)
vegetables_sold

# %%
def clear(percent,sum,vegetables_sold):
    cur=0
    i=0
    while cur < percent:
        cur+=vegetables_sold.loc[i,"单品销售量"]/sum
        i+=1
    return vegetables_sold.iloc[:i,:]

# %%
vegetables_sold = clear(0.95,vegetables_sold.loc[:,"单品销售量"].sum(),vegetables_sold)
vegetables_sold

# %%
condition = df['单品编码'].isin(vegetables_sold["单品编码"].unique())

# 根据条件删除不符合条件的行
df_filtered = df[condition]
df_filtered

# %%
all_vegetables=pd.Series(df_filtered["单品编码"].unique())
all_kinds = pd.Series(df_filtered["分类编码"].unique())

kinds_sold = pd.DataFrame(columns=["分类编码","单类销售量"])
kinds_sold["分类编码"]= all_kinds
kinds_sold["单类销售量"] = 0
kinds_sold

# %%
def compute_sold_2(df,all,sold):
    for i in range(len(all)):
        sold.iloc[i,1]=df.loc[(df["分类编码"] == all[i]) ,["销量(千克)"]].sum() 
    return sold
#计算分类销售量

# %%
kinds_sold = compute_sold_2(df,all_kinds,kinds_sold)
kinds_sold

# %%
df_filtered.to_excel("数据清洗后.xlsx",index=False)

# %%
def figure_Day(df,df_time):
    dateRange = df["销售日期"].unique()
    one_day = np.timedelta64(1, 'D')
    for i in range(len(dateRange)):
        for j in range(df_time.shape[1]-1):
            condition1 = (df["销售时间"] >= dateRange[i]) & (df["销售时间"] < dateRange[i]+one_day) & (df["单品编码"] == df_time.columns[j+1])
            df_time.iloc[i,j+1]=df.loc[condition1,"销量(千克)"].sum()
    return df_time

# %%
dateRange = df["销售日期"].unique()
df_day = pd.DataFrame(dateRange,columns=["Date"])
for name in all_vegetables:
    df_day[name] = 0
df_day = figure_Day(df_filtered,df_day)
df_day

# %%
all_vegetables=pd.Series(df_filtered["单品名称"].unique())
df_day_copy = df_day
new_dict = {}
for code,items in zip(df_filtered["单品编码"].unique(),df_filtered["单品名称"].unique()):
    new_dict[code]=items
new_dict
df_day_copy.rename(columns=new_dict, inplace=True)
df_day_copy

# %%
df_day_copy.to_excel("日销量.xlsx",index=False)

# %%

#df_day['Date'] = pd.to_datetime(df_day['Date'])
R=range(df_day.shape[0])
for j in range(1,df_day.shape[1]):
# 创建图表
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300,facecolor='white')  # 设置图表的尺寸和分辨率

# 设置字体以支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

# 绘制曲线图，这里使用自定义的R变量
    
    ax.plot(df_day['Date'].iloc[R], df_day[df_day.columns[j]].iloc[R], label=df_day.columns[j])

# 设置X轴刻度
    custom_xticks = df_day['Date'].iloc[R][::10]  # 自定义X轴刻度间隔
    ax.set_xticks(custom_xticks)
    ax.tick_params(axis='x', rotation=90)  # 设置X轴刻度标签旋转角度

# 添加图例
    ax.legend(loc='upper right')
    plt.xlabel("日期")
    plt.ylabel("日销量/千克")
# 显示图形
    plt.tight_layout()  # 自动调整布局以防止标签被裁剪
    plt.savefig("outPNG/{}.png".format(df_day.columns[j]), dpi=300)  # 保存图像为文件（可选）
    plt.close()


# %%
from pandas.plotting import scatter_matrix
scatter_matrix(df_day.iloc[:, 1:49], figsize=(15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=0.8,cmap=mglearn.cm3)

# %%
grouped = df_filtered.groupby("分类名称")
df_day_copy = df_day.copy()
for name, group_data in grouped:
    # 获取同一分类下的单品名称列表
    single_products = group_data["单品名称"].unique()
    
    # 在df_day_copy中添加一列，该列的值为同一分类下所有单品的销售量之和
    df_day_copy[name] = df_day_copy[single_products].sum(axis=1)
    

# %%
df_day_copy.iloc[:, [0] + list(range(-1, -7, -1))].to_excel("品类日销量.xlsx",index=False)

# %%
# 创建一个白色背景的坐标系
fig, ax = plt.subplots(figsize=(15, 15))
ax.set_facecolor('white')  # 设置背景颜色为白色

# 绘制散点矩阵
scatter_matrix = pd.plotting.scatter_matrix(df_day_copy.iloc[:, list(range(-1, -7, -1))], ax=ax,
                                            marker='o', hist_kwds={'bins': 20}, s=60, alpha=0.8, cmap=mglearn.cm3)

# 如果需要，可以进一步自定义散点矩阵的样式
# 例如，可以设置对角线上的图形，添加标签等
for ax in scatter_matrix.ravel():
    ax.set_xlabel(ax.get_xlabel(), fontsize=12)
    ax.set_ylabel(ax.get_ylabel(), fontsize=12)

plt.show()

# %%
vegetables_sold['单品名称'] = vegetables_sold['单品编码'].map(new_dict)
vegetables_sold.iloc[:,[1,2]].to_excel("选择的单品.xlsx",index=False)

# %%
plt.figure(dpi=300)
for i in range(1, 7):
    plt.plot(df_day_copy['Date'].iloc[:], df_day_copy[df_day_copy.columns[-i]].iloc[:], label=df_day_copy.columns[-i])
    plt.legend(loc='upper right',fontsize=10)
# 设置图像分辨率为 300 dpi 
    plt.savefig("outPNG/{}.png".format(df_day_copy.columns[-i]), facecolor='white')
    plt.clf()

# 添加图例
#plt.legend(loc='upper right',fontsize=100)

# %%



