#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
data = pd.read_excel('D:/qq/聊天文件/销量预测.xlsx')
print(data.head())


# In[9]:


data1 = pd.read_excel('D:/qq/聊天文件/附件1.xlsx')
print(data1.head())


# In[7]:




# 将表二的蔬菜名称和分类信息作为字典
classification_dict = dict(zip(data1['单品名称'], data1['分类名称']))

# 修改表一的列名
data.rename(columns=classification_dict, inplace=True)

# 打印修改后的DataFrame
print(data)


# In[13]:


data2 = pd.read_excel('D:/qq/聊天文件/批发价预测.xlsx')
print(data2.head())


# In[14]:


combined_df = pd.concat([data, data2], ignore_index=True)

# 打印连接后的数据
print(combined_df)


# In[31]:


import pandas as pd
data = pd.read_excel('D:/qq/聊天文件/用于计算.xlsx')
print(data.head())


# In[62]:


data['1日进货量']=data['1日销量']/(1-data['损耗率(%)']/100)
data['2日进货量']=data['2日销量']/(1-data['损耗率(%)']/100)
data['3日进货量']=data['3日销量']/(1-data['损耗率(%)']/100)
data['4日进货量']=data['4日销量']/(1-data['损耗率(%)']/100)
data['5日进货量']=data['5日销量']/(1-data['损耗率(%)']/100)
data['6日进货量']=data['6日销量']/(1-data['损耗率(%)']/100)
data['7日进货量']=data['7日销量']/(1-data['损耗率(%)']/100)
data


# In[33]:


data['1日销售额']=data['1日成本']*(1+data['利润率'])
data['2日销售额']=data['2日成本']*(1+data['利润率'])
data['3日销售额']=data['3日成本']*(1+data['利润率'])
data['4日销售额']=data['4日成本']*(1+data['利润率'])
data['5日销售额']=data['5日成本']*(1+data['利润率'])
data['6日销售额']=data['6日成本']*(1+data['利润率'])
data['7日销售额']=data['7日成本']*(1+data['利润率'])
data


# In[34]:


df = pd.DataFrame(data)


# In[63]:


result = df.groupby('分类名称').agg({'1日销量': 'sum', '1日销售额': 'sum', '1日成本': 'sum','1日进货量': 'sum','2日销量': 'sum', '2日销售额': 'sum','2日成本': 'sum','2日进货量': 'sum','3日销量': 'sum', '3日销售额': 'sum','3日成本': 'sum','3日进货量': 'sum','4日销量': 'sum', '4日销售额': 'sum','4日成本': 'sum','4日进货量': 'sum','5日销量': 'sum','5日销售额': 'sum','5日成本': 'sum','5日进货量': 'sum','6日销量': 'sum', '6日销售额': 'sum','6日成本': 'sum','6日进货量': 'sum','7日销量': 'sum', '7日销售额': 'sum','7日成本': 'sum','7日进货量': 'sum',}).reset_index()
result


# In[64]:


import pandas as pd
data2 = pd.read_excel('D:/qq/折扣力度.xlsx')
data2


# In[65]:


data2 = pd.DataFrame(data2)
result2 = pd.merge(result, data2, on=['分类名称'], how='inner')
result2


# In[66]:


result2['1日定价']=result2['1日销售额']/(result2['1日销量']*(1+result2['折扣系数']))
result2['2日定价']=result2['2日销售额']/(result2['2日销量']*(1+result2['折扣系数']))
result2['3日定价']=result2['3日销售额']/(result2['3日销量']*(1+result2['折扣系数']))
result2['4日定价']=result2['4日销售额']/(result2['4日销量']*(1+result2['折扣系数']))
result2['5日定价']=result2['5日销售额']/(result2['5日销量']*(1+result2['折扣系数']))
result2['6日定价']=result2['6日销售额']/(result2['6日销量']*(1+result2['折扣系数']))
result2['7日定价']=result2['7日销售额']/(result2['7日销量']*(1+result2['折扣系数']))
result2


# In[67]:


result2.to_excel('D:/qq/聊天文件/output2.xlsx', index=False) 


# In[1]:


import pandas as pd
data = pd.read_excel('D:/qq/聊天文件/限制选择的单品.xlsx')
data


# In[39]:


data1 = pd.read_excel('D:/qq/聊天文件/批发价1号预测.xlsx')
data1
data2 = pd.read_excel('D:/qq/附件四修改版.xlsx')
data2


# In[43]:


data = pd.DataFrame(data)
data1 = pd.DataFrame(data1)
data2 = pd.DataFrame(data2)
result = pd.merge(data, data1, on=['单品名称'], how='left')
result1 = pd.merge(result, data2, on=['单品名称'], how='left')
result1


# In[45]:


result1['成本']=result1['2023-07-01']/(1-result1['损耗率(%)']/100)
result1


# In[48]:


result1 = result1.sort_values(by='成本', ascending=True)
result1


# In[49]:


result1.to_excel('D:/qq/聊天文件/问题三.xlsx', index=False) 


# In[61]:


result2 = pd.read_excel('D:/qq/聊天文件/问题三 (1).xlsx')
result2


# In[62]:


data = pd.read_excel('D:/qq/聊天文件/单品利润率.xlsx')
data
data1 = pd.read_excel('D:/qq/折扣力度.xlsx')
data1


# In[64]:


result2 = pd.DataFrame(result2)
data = pd.DataFrame(data)
data1 = pd.DataFrame(data1)
result2 = pd.merge(result2, data, on=['单品名称'], how='left')
result2 = pd.merge(result2, data1, on=['分类名称'], how='left')
result2


# In[66]:


result2['定价']=result2['成本']*(1+result2['利润率_x'])/(1+result2['折扣系数_x'])
result2


# In[67]:


result2.to_excel('D:/qq/聊天文件/单品定价.xlsx', index=False) 


# In[ ]:




