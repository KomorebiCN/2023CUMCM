# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn
#读取附件一
df1 = pd.read_excel("附件1.xlsx")
df1["单品编码"] = df1["单品编码"].astype(str)
df1["分类编码"] = df1["分类编码"].astype(str)
#读取附件二
df2 = pd.read_excel("附件2.xlsx")
df2["单品编码"] = df2["单品编码"].astype(str)
#按单品编码合并
df = pd.merge(df2,df1,on="单品编码")
df = df[df['销售类型'] != '退货']#删除退货的数据
#计算销售具体时间
df['扫码销售时间'] = pd.to_timedelta(df['扫码销售时间'])
df["销售时间"]= df["销售日期"]+df["扫码销售时间"]
#df=df.drop(columns=["销售日期","扫码销售时间"])
df=df.sort_values(by="销售时间").reset_index(drop=True)


# %%
all_vegetables=pd.Series(df["单品名称"].unique())
df

# %% [markdown]
# #计算各单品日销量

# %%
dateRange=df["销售日期"].unique()


# %%
#def figure_Day(df,df_time,dateRange):
#    one_day = np.timedelta64(1, 'D')
#    for i in range(len(dateRange)):
#        for j in range(df_time.shape[1]-1):
#            condition1 = (df["销售时间"] >= dateRange[i]) & (df["销售时间"] < dateRange[i]+one_day) & (df["单品名称"] == df_time.columns[j+1])
#            df_time.iloc[i,j+1]=df.loc[condition1,"销量(千克)"].sum()
#    return df_time

# %%
#df_day = pd.DataFrame(dateRange,columns=["Date"])
#for name in all_vegetables:
#    df_day[name] = 0
#df_day = figure_Day(df,df_day,dateRange)
#df_day

# %%
def figure_Day(df, df_time, dateRange):
    # 将销售时间列转换为 datetime64 数据类型
    df['销售时间'] = pd.to_datetime(df['销售时间'])
    
    # 将日期范围添加到数据框中
    df['日期范围'] = pd.cut(df['销售时间'], bins=dateRange, right=False, labels=False)
    
    # 使用 pivot_table 执行汇总操作
    pivot_df = pd.pivot_table(df, index=['日期范围', '单品名称'], values='销量(千克)', aggfunc='sum').unstack(fill_value=0)
    
    # 将结果填充到 df_time 中
    df_time.iloc[:, 1:] = pivot_df.values
    
    # 删除日期范围列
    df.drop(columns=['日期范围'], inplace=True)
    
    return df_time

# %%



