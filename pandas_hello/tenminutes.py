#/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
本文是对pandas官方网站上《10 Minutes to pandas》的一个简单的翻译，原文在http://pandas.pydata.org/pandas-docs/stable/10min.html
详细内容在：http://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook
'''

import pandas as pd 
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 

# 一、创建对象
# 可以通过传递一个list对象来创建一个Series，pandas会默认创建整型索引
s = pd.Series([1,2,4,5,6,7,9])
print(s)

# 通过传递一个numpy array，时间索引以及列标签来创建一个DataFrame：
dates = pd.date_range('20150901',periods=6)
print(dates)
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
print(df)

# 通过传递一个能够被转换成类似序列结构的字典对象来创建一个DataFrame：
df2 = pd.DataFrame({'A':1,
	               'B':pd.Timestamp('20150901'),
	               'C':pd.Series(1,index=list(range(4)),dtype='float32'),
                   'D':np.array([3]*4,dtype='int32'),
                   'E':pd.Categorical(['test','train','test','train']),
                   'F':'foo'}
	               )

print(df2)

print('-----------------------df2.dtypes-----------------------')
print(df2.dtypes)


# http://pandas.pydata.org/pandas-docs/stable/basics.html#basics
# 二、查看数据
# 1、  查看frame中头部和尾部的行：
print('-----------------------df.head()-----------------------')
print(df.head())
print('-----------------------df.tail(3)-----------------------')
print(df.tail(3))

# 2、  显示索引、列和底层的numpy数据：

print(df.index)


print(df.columns)


print(df.values)

# 3、  describe()函数对于数据的快速统计汇总：

print(df.describe)

# 4、  对数据的转置：
print(df.T)


# 5、  按轴进行排序
print(df.sort_index(axis=1,ascending=False))


# 6、 按值进行排序
print(df.sort(columns='B'))


# 三、 选择
# 虽然标准的Python/Numpy的选择和设置表达式都能够直接派上用场，但是作为工程使用的代码，我们推荐使用经过优化的pandas数据访问方式： .at, .iat, .loc, .iloc 和 .ix详情请参阅Indexing and Selecing Data 和 MultiIndex / Advanced Indexing。

# l  获取

# 1、 选择一个单独的列，这将会返回一个Series，等同于df.A：
print(df['A'])

# 2、 通过[]进行选择，这将会对行进行切片
print(df[0:3])

print(df['20150902':'20150904'])

# 通过标签选择

# 1、 使用标签来获取一个交叉的区域
print(df.loc[dates[0]])


# 2、 通过标签来在多个轴上进行选择
print(df.loc[:,['A','B']])

# 3、 标签切片
print(df.loc['20150902':'20150904',['A','B']])

# 4、对于返回的对象进行维度缩减
print(df.loc['20150902',['A','B']])

# 5、获取一个标量
print(df.loc[dates[0],'A'])

# 6、快速访问一个标量（与上一个方法等价）
print(df.at[dates[0],'A'])

#  通过位置选择

# 1、 通过传递数值进行位置选择（选择的是行）
print(df.iloc[3])

# 2、 通过数值进行切片，与numpy/python中的情况类似
print(df.iloc[3:5,0:2])

# 3、 通过指定一个位置的列表，与numpy/python中的情况类似
print(df.iloc[[1,2,3],[0,2]])

# 4、 对行进行切片
print(df.iloc[1:3,:])

# 5、 对列进行切片
print(df.iloc[:,1:3])

# 6、获取特定的值
print(df.iloc[1,1])
print(df.iat[1,1])

# 布尔索引

# 1、 使用一个单独列的值来选择数据：
print(df[df.A>0])

# 2、 使用where操作来选择数据：
print(df[df>0])

# 3、 使用isin()方法来过滤：
print(df2[df2['E'].isin(['test'])])

# 设置

# 1、 设置一个新的列：
s1 = pd.Series([1,2,3,4,5,6],index=pd.date_range('20150901',periods=6))
print(s1)

# 2、 通过标签设置新的值：
df.at[dates[0],'A'] = 0
print(df)

# 3、 通过位置设置新的值：
df.iat[0,1] = 0

# 4、 通过一个numpy数组设置一组新值：
df.loc[:,'D'] = np.array([5]*len(df))

print(df)

# 5、 通过where操作来设置新的值：
df5 = df.copy()
df5[df5>0] = -df5
print(df5)

# 四、            缺失值处理
# 在pandas中，使用np.nan来代替缺失值，这些值将默认不会包含在计算中，详情请参阅：Missing Data Section。

# 1、  reindex()方法可以对指定轴上的索引进行改变/增加/删除操作，这将返回原始数据的一个拷贝：、
df1 = df.reindex(index=dates[0:4],columns=list(df.columns)+['E'])
df1.loc[dates[0]:dates[1],'E'] = 1
print(df1)

# 2、  去掉包含缺失值的行：
print('-------------------df1 = df1.dropna(how=\'any\')--------------------------')
df1 = df1.dropna(how='any')
print(df1)

# 3、  对缺失值进行填充：
df1 = df.reindex(index=dates[0:4],columns=list(df.columns)+['E'])
df1.loc[dates[0]:dates[1],'E'] = 1
df1 = df1.fillna(value='default')
# df1 = df1.fillna(value=1)
print(df1)

# 4、  对数据进行布尔填充：
# pd.isnull(df1)
# print(pd)

# 五、            相关操作
# 详情请参与 Basic Section On Binary Ops

# 统计（相关操作通常情况下不包括缺失值）

# 1、  执行描述性统计：
print(df.mean)

# 2、  在其他轴上进行相同的操作：
print(df.mean(1))

# 3、  对于拥有不同维度，需要对齐的对象进行操作。Pandas会自动的沿着指定的维度进行广播：
s = pd.Series([1,3,5,np.nan,6,8],index=dates).shift(2)
print(s)

print(df.sub(s,axis='index'))

# Apply

# 1、  对数据应用函数：
df.apply(np.cumsum)
df.apply(lambda x:x.max() - x.min())

# 直方图
s = pd.Series(np.random.randint(0,7,size=10))
print(s)

# 字符串方法

# Series对象在其str属性中配备了一组字符串处理方法，可以很容易的应用到数组中的每个元素，如下段代码所示。更多详情请参考：Vectorized String Methods.

s = pd.Series(['A','B','C','Aaba','Bas',np.nan,'CABA','dog','cat'])
s.str.lower()

# 六、            合并
# Pandas提供了大量的方法能够轻松的对Series，DataFrame和Panel对象进行各种符合各种逻辑关系的合并操作。具体请参阅：Merging section

# l  Concat








# 十一、           画图
# 具体文档参看：Plotting docs   http://pandas.pydata.org/pandas-docs/stable/visualization.html#visualization
ts = pd.Series(np.random.randn(1000),index=pd.date_range('1/9/2015',periods=1000))
ts = ts.cumsum()
ts.plot()
# print(ts)
# 对于DataFrame来说，plot是一种将所有列及其标签进行绘制的简便方法：
df = pd.DataFrame(np.random.randn(1000,4),index=ts.index,columns=['A','B','C','D'])
df = df.cumsum()
plt.figure();df.plot();


















































































