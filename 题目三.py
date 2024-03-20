# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

df=pd.read_excel("数据清洗后.xlsx")

# %%
df_forcast = pd.read_excel("销量预测.xlsx")
df_forcast

# %%
df_zhesun=pd.read_excel("附件4s.xlsx")
map_dict={}
for name,num in zip(df_zhesun.iloc[:,1],df_zhesun.iloc[:,2]):
    map_dict[name]=num
map_dict

# %%
df_solds = df_forcast.copy()

# %%
for i in range(df_forcast.shape[0]):
    for j in range(1,df_forcast.shape[1]):
        df_forcast.iloc[i,j]=df_forcast.iloc[i,j]/(1-map_dict[df_forcast.columns[j]]/100)
df_forcast

# %%
df_forcast=df_forcast.T


# %%
df_forcast

# %%
df_forcast["预测销量"]=df_solds.iloc[0,:]
df_forcast

# %%
df_forcast.rename(columns={0:"补货量"}, inplace=True)
df_forcast

# %%
df_forcast.reset_index(drop=False, inplace=True)
df_forcast.rename(columns={"index":"单品名称"}, inplace=True)
df_forcast

# %%
df_forcast=df_forcast.iloc[:,[0,1,-1]]
df_forcast

# %%
df_forcast=df_forcast.iloc[1:,:]

# %%
df_forcast["是否>=2.5kg"]=0
for i in range(df_forcast.shape[0]):
    if df_forcast.iloc[i,1] >= 2.5:
        df_forcast.iloc[i,-1] =1
df_forcast

# %%
df_forcast.reset_index(drop=True, inplace=True)
df_forcast

# %%
df_day=pd.read_excel("日销量.xlsx")
df_day

# %%
df_day=df_day.iloc[-7:,:]
df_day

# %%
for name in df_day.columns[1:]:
    if df_day.loc[:, name].sum() == 0:
        df_day.drop(columns=[name], inplace=True)
df_day

# %%
left_vege = df_day.columns[1:]
left_vege

# %%
df_forcast_cl = df_forcast[df_forcast['单品名称'].isin(left_vege.to_list())]
df_forcast_cl

# %%
df_forcast_cl.reset_index(drop=True, inplace=True)

# %%
df_forcast_cl

# %%
df_forcast_cl.iloc[:,-1].sum()

# %%
chosen_vege = df_forcast_cl.loc[df_forcast_cl["是否>=2.5kg"] == 1,"单品名称"]

# %%
chosen_vege = chosen_vege.to_list()
chosen_vege

# %%
category = pd.read_excel("附件1.xlsx")
grouped = category.groupby("分类名称")
new_dict = {}
for name,group_data in grouped:
    single_products = group_data["单品名称"].unique()
    for key in single_products:
        new_dict[key] = name
new_dict

# %%
df_forcast_cl["分类名称"]=df_forcast_cl.loc[:,"单品名称"].map(new_dict)
df_forcast_cl

# %%
grouped = df_forcast_cl.groupby("分类名称")
new_dict = {}
for name,group_data in grouped:
    new_dict[name]=group_data.loc[group_data["是否>=2.5kg"] == 1,"预测销量"].sum()
new_dict

# %%
grouped = category.groupby("分类名称")
cate = {}
for name,group_data in grouped:
    single_products = group_data["单品名称"].unique()
    for key in single_products:
        cate[key] = name
cate

# %%
old_dict = {'水生根茎类':0.1479,'花叶类':0.4241,'花菜类':0.0555,'茄类':0.0648,'辣椒类':0.2629,'食用菌':0.0449}#手动计算占比

# %%
ssum=0
for key in df_forcast_cl["分类名称"].unique():
    ssum+=new_dict[key]
ssum

# %%
new_percent={}
for key in df_forcast_cl["分类名称"].unique():
    new_percent[key] = new_dict[key]/ssum
new_percent

# %%
dict1 = old_dict
dict2 = new_percent


from matplotlib.font_manager import FontProperties

# 指定中文字体
font = FontProperties(fname="C:/Windows/Fonts/msyh.ttc", size=12)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 替换为你选择的中文字体
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
plt.figure(figsize=(8, 6), dpi=300, facecolor='white')
# 确定统一的键顺序（这里按照 dict1 的键顺序）
keys = dict1.keys()

# 提取字典中的值
values1 = [dict1[key] for key in keys]
values2 = [dict2[key] for key in keys]

# 设置条形图的位置
x = range(len(keys))

# 绘制条形图
plt.bar(x, values1, width=0.4, label='前7日占比', align='center')
plt.bar(x, values2, width=0.4, label='预测占比', align='edge')

# 设置 x 轴标签，并使用中文字体
plt.xticks(x, keys, fontproperties=font)

# 添加图例
plt.legend()

# 添加标题和标签，并使用中文字体
plt.title('占比统计', fontproperties=font)
plt.xlabel('分类名称', fontproperties=font)
plt.ylabel('占比', fontproperties=font)


# %%
old_df = pd.read_excel("品类日销量.xlsx")
old_df = old_df.iloc[-7:,:]
old_df

# %%
mean_amount={}
for i in range(1,len(old_df.columns)):
    mean_amount[old_df.columns[i]]=old_df.iloc[-1,i]
mean_amount

# %%
grouped = df_forcast_cl.groupby("分类名称")
new_dict_nodelete = {}
for name,group_data in grouped:
    new_dict_nodelete[name]=group_data.loc[:,"预测销量"].sum()
new_dict_nodelete

# %%
dict1 = mean_amount
dict2 = new_dict
dict3 = new_dict_nodelete
plt.figure(figsize=(8, 6), dpi=300, facecolor='white')
# 确定统一的键顺序（这里按照 dict1 的键顺序）
keys = dict1.keys()

# 提取字典中的值
#values1 = [dict1[key] for key in keys]
values2 = [dict2[key] for key in keys]
values3 = [dict3[key] for key in keys]
# 设置条形图的位置
x = range(len(keys))

# 绘制条形图
plt.figure(figsize=(10, 6), dpi=300, facecolor='white')
#plt.bar(x, values1, width=0.2, label='某日', align='center')
plt.bar([i + 0.2 for i in x], values2, width=0.2, label='预测', align='center')
plt.bar([i + 0.4 for i in x], values3, width=0.2, label='非删减预测', align='center')

# 设置 x 轴标签
plt.xticks([i + 0.2 for i in x], keys, rotation=45, fontsize=8)

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('销量统计')
plt.xlabel('分类名称')
plt.ylabel('销量/千克')

# 显示图形
plt.tight_layout()
plt.show()

# %%
df_forcast_cl.to_excel("限制选择的单品.xlsx",index=False)

# %%
new_dict["茄类"]+=2.1787440176
new_dict["食用菌"]+=1.9316905093

dict1 = mean_amount
dict2 = new_dict
dict3 = new_dict_nodelete
plt.figure(figsize=(8, 6), dpi=300, facecolor='white')
# 确定统一的键顺序（这里按照 dict1 的键顺序）
keys = dict1.keys()

# 提取字典中的值
#values1 = [dict1[key] for key in keys]
values2 = [dict2[key] for key in keys]
values3 = [dict3[key] for key in keys]
# 设置条形图的位置
x = range(len(keys))

# 绘制条形图
plt.figure(figsize=(10, 6), dpi=300, facecolor='white')
#plt.bar(x, values1, width=0.2, label='某日', align='center')
plt.bar([i + 0.2 for i in x], values2, width=0.2, label='预测', align='center')
plt.bar([i + 0.4 for i in x], values3, width=0.2, label='非删减预测', align='center')

# 设置 x 轴标签
plt.xticks([i + 0.2 for i in x], keys, rotation=45, fontsize=8)

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('销量统计')
plt.xlabel('分类名称')
plt.ylabel('销量/千克')

# 显示图形
plt.tight_layout()
plt.show()

# %%



