#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[5]:


excel_file_path = 'D:/qq/聊天文件/数据清洗后.xlsx'

# 使用pandas的read_excel方法导入Excel文件
data = pd.read_excel(excel_file_path)


# In[6]:


print(data.head()) 


# In[7]:


sorted_data = data.sort_values(by='销售单价(元/千克)')


# In[8]:


print(sorted_data.head())


# In[9]:


grouped_data = data.groupby('分类名称')


# In[10]:


for category, group in grouped_data:
    # 使用category和group进行操作，例如打印分类名和数据
    print(f"Category: {category}")
    print(group)


# In[11]:


discount_ratio = grouped_data['是否打折销售'].apply(lambda x: x.map({'是': True, '否': False}).mean())

# 打印每个组中的打折比例
print(discount_ratio)


# In[12]:


import pandas as pd

# 假设您已经按照分类名称分组并存储在grouped_data中

# 创建一个新的DataFrame来存储结果
result_data = pd.DataFrame()

# 计算每个分类内是否打折的数量，并将结果转换为布尔值
result_data['是否打折销售'] = grouped_data['是否打折销售'].transform(lambda x: x.eq('是').any())

# 计算每个分类内的折扣率
def calculate_discount_rate(group):
    if group['是否打折销售'].any():
        discount_mean = group.loc[group['是否打折销售'], '销售单价(元/千克)'].mean()
        group['折扣率'] = 1 - group['销售单价(元/千克)'] / discount_mean
    else:
        group['折扣率'] = 0  # 如果没有打折数据，则折扣率为0
    return group

result_data = grouped_data.apply(calculate_discount_rate)

# 使用groupby()按照'分类名称'列进行分组，并计算每个分类的平均折扣率
average_discount_rate = result_data.groupby('分类名称')['折扣率'].mean().reset_index()


# 打印每个分类的平均折扣率
print(average_discount_rate)


# In[13]:


import pandas as pd
excel_file_path2 = 'D:/qq/附件四修改版.xlsx'
# 使用read_excel导入数据
data2 = pd.read_excel('D:/qq/附件四修改版.xlsx')


# In[14]:


print(data2.head())


# In[15]:


table1 = pd.DataFrame(data)
table2 = pd.DataFrame(data2)


# In[16]:


merged_data = pd.merge(table1, table2, on=['单品名称', '单品编码'], how='left')
merged_data


# In[17]:


import pandas as pd
excel_file_path3 = 'D:/qq/聊天文件/附件3.xlsx'
# 使用read_excel导入数据
data3 = pd.read_excel('D:/qq/聊天文件/附件3.xlsx')
print(data3.head())


# In[18]:


table3 = pd.DataFrame(data3)
merged_data3 = pd.merge(merged_data, table3, on=['销售日期', '单品编码'], how='left')
merged_data3


# In[19]:


merged_data3['利润']=merged_data3['销量(千克)']*merged_data3['销售单价(元/千克)']-merged_data3['批发价格(元/千克)']*merged_data3['销量(千克)']/(1-merged_data3['损耗率(%)']/100)


# In[20]:


merged_data3


# In[21]:


merged_data3['成本']=merged_data3['批发价格(元/千克)']*merged_data3['销量(千克)']/(1-merged_data3['损耗率(%)']/100)


# In[22]:


merged_data3


# In[27]:


result = merged_data3.groupby('单品名称')['利润'].sum().reset_index()
result


# In[28]:


result1 = merged_data3.groupby('单品名称')['成本'].sum().reset_index()
result1


# In[34]:


result2 = pd.merge(result, result1, on=['单品名称'], how='inner')
result2['利润率']=result2['利润']/result2['成本']
result2
result2.to_excel('D:/qq/聊天文件/单品利润率.xlsx', index=False) 


# In[25]:


import pandas as pd
data_sale = pd.read_excel('D:/qq/聊天文件/日销量.xlsx')
print(data_sale.head())


# In[39]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[40]:


import matplotlib.pyplot as plt

# 示例数据
categories = ['1日收益', '2日收益', '3日收益', '4日收益', '5日收益', '6日收益', '7日收益']
values = [649.6865139, 608.6804961, 601.5645523, 603.8445866, 613.6927919, 618.5767892, 624.3340563]

# 创建一个条形图
sns.barplot(x=categories, y=values)

# 添加标题和标签
plt.title('未来七日收益')
plt.xlabel('日期')
plt.ylabel('收益')

# 显示图形
plt.show()


# In[26]:


df = pd.DataFrame(data_sale)

# 转换月份列为日期时间类型
df['Date'] = pd.to_datetime(df['Date'])

# 创建虚拟变量（独热编码）以处理分类变量
df = pd.get_dummies(df, columns=['蔬菜分类'], drop_first=True)

# 添加截距项
df['截距'] = 1

# 定义自变量（特征）和因变量
X = df[['截距', '蔬菜分类_蔬菜B', '蔬菜分类_蔬菜C', '月份']]
y = df['销售量']

# 拟合多元回归模型
model = sm.OLS(y, X).fit()

# 打印回归结果
print(model.summary())


# In[ ]:




