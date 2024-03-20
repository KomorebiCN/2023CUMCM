# %%
import pmdarima as pm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

df1=pd.read_excel("批发价预测.xlsx")
df1 = df1.add_prefix('批发_')
df2=pd.read_excel("销量预测.xlsx")
df2 = df2.add_prefix('销量_')
df=pd.concat([df1, df2.iloc[:,1:]], axis=1)
df = df.rename(columns={'批发_Date': 'Date'})
df_copy=df.T.copy()

# %%


# %%
df_filtered = pd.read_excel("数据清洗后.xlsx")
grouped = df_filtered.groupby("分类名称")
new_dict={}
for name, group_data in grouped:
    # 获取同一分类下的单品名称列表
    single_products = group_data["单品名称"].unique()
    for j in single_products:
        new_dict["批发_{}".format(j)]= name
        new_dict["销量_{}".format(j)]= name



# %%
df_copy['分类名称'] = df_copy.index.map(new_dict)
df_copy

# %%
new_dict={}
for name, group_data in grouped:
    # 获取同一分类下的单品名称列表
    single_products = group_data["单品名称"].unique()
    for j in single_products:
        new_dict[j]= name

# %%
df_lirun = pd.read_excel("利润率.xlsx") 
df_lirun

# %%
lirun_dict={}
for i in range(6):
    lirun_dict[df_lirun.iloc[i,0]]=df_lirun.iloc[i,3]

# %%
df_copy['利润率'] = df_copy['分类名称'].map(lirun_dict)
df_copy

# %%
df_zhesun = pd.read_excel("附件4s.xlsx")
df_zhesun 

# %%
zhesun_dict={}
for i in range(251):
    zhesun_dict["批发_"+df_zhesun.iloc[i,1]]=df_zhesun.iloc[i,2]
    zhesun_dict["销量_"+df_zhesun.iloc[i,1]]=df_zhesun.iloc[i,2]

# %%
df_copy['损耗率(%)'] = df_copy.index.map(zhesun_dict)
df_copy

# %%
df_copy.to_excel("用于计算.xlsx")

# %%



