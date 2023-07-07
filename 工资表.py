import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt

df1 = pd.read_excel(r'D:\育英-数据处理集训\04-test\pandas120.xlsx',sheet_name='Sheet1')

# 1） 将salary列的数据转换为最大值和最小值的平均值。举例说明：第一列数据‘20k-35k’转换为27500。
def fun_sal(x):
    a,b = x.split('-') # 按指定符号将工资进行拆分
    a = int(a.strip('k'))*1000 # 去掉k再乘以1000
    b = int(b.strip('k'))*1000
    return (a+b)/2
df1['salary'] = df1['salary'].map(fun_sal)  # .apply(fun_sal)
print(df1.head())
with pd.ExcelWriter(r'D:\育英-数据处理集训\04-test\pandas120.xlsx',engine='openpyxl',mode='a',if_sheet_exists='overlay') as writer:
    df1.to_excel(writer,sheet_name='Sheet1',index=False)


# 3） 将createTime列转换为月日（不保留年和具体的时间信息）。
# 方法一
df1['createTime'] = df1['createTime'].map(lambda x:x.strftime('%m-%d'))
# 方法二
df1['createTime'] = df1['createTime'].dt.strftime('%m月%d日')
with pd.ExcelWriter(r'D:\育英-数据处理集训\04-test\pandas120.xlsx',engine='openpyxl',mode='a',if_sheet_exists='overlay') as writer:
    df1.to_excel(writer,sheet_name='Sheet1',index=False)


# 5） 查看数值型列的汇总统计，包括数量、平均值、标准差、最小值、最大值、25%、50%、75%分位数等信息。
print(df1['salary'].describe())

# 6） 新增一列（列名：‘categories’）根据salary将数据分为三组，并设置等级。其中[0,5000)为‘底’，[5000,20000)为‘中’，[20000，max]为‘高’。
# 方法一：map()
def cate(x):
    if x>0 and x<5000:
        return '低'
    elif x>=5000 and x<20000:
        return '中'
    else:
        return '高'
df1['categories'] = df1['salary'].map(cate)
print(df1)
# 方法二：pd.cut()
bins=[0,5000,20000,50000] # 划分区间
group_names=['低','中','高']
df1['categories'] =pd.cut(df1['salary'],bins,labels=group_names)

with pd.ExcelWriter(r'D:\育英-数据处理集训\04-test\pandas120.xlsx',engine='openpyxl',mode='a',if_sheet_exists='overlay') as writer:
    df1.to_excel(writer,sheet_name='Sheet1',index=False)


# 9） 根据categories列的信息，绘制饼图，以直观展示底、中、高的占比。要求同时显示值与百分比。
# 准备制图的数据，自定义排序顺序
df = df1.groupby('categories',as_index=False)['education'].count()
df['order'] = df['categories'].map({'低':1,'中':2,'高':3})
df.sort_values('order',inplace=True,ignore_index=True)
# print(df)
'''---------pie----------'''
total = sum(df['education'])
plt.rcParams['font.sans-serif']=['KaiTi']
# 显示值和百分比
def pct_format(pct):
    val = int(total*pct/100)
    return '{:d}，{:.2f}%'.format(val,pct)
plt.pie(df['education'],labels=df['categories'],autopct=pct_format,counterclock=False,shadow=True,labeldistance=1.2)
plt.title('工资等级占比饼图',fontsize=18,fontweight='bold')
plt.legend(loc=10,bbox_to_anchor=(0,0,2.3,1.8)) # 微调图例的显示位置
plt.show()
'''---------plot----------'''
# plt.rcParams['font.sans-serif']=['KaiTi']
# plt.plot(df['categories'],df['education'],linewidth=1,linestyle='dashdot',marker='o',markersize=5,color='k')
# for a,b in zip(range(3),df['education']):
#     plt.text(a,b,b,ha='center',va='bottom',size=11)
# plt.grid(True) # 显示点状网格线，默认的
# plt.title('工资等级占比饼图',fontsize=18,fontweight='bold')
# plt.show()
'''---------barh----------'''
# plt.rcParams['font.sans-serif']=['KaiTi']
# plt.barh(df['categories'],df['education'],height=0.2,align='center')
# for a,b in zip(range(3),df['education']):
#     plt.text(b,a,b,ha='left',va='center') # 注意要把a,b的位置调换下，b在x轴而a在y轴
# plt.show()
'''---------scatter----------'''
# plt.rcParams['font.sans-serif'] = ['KaiTi']
# colors = df['education'] * 10  # 根据y值生成不同的颜色
# area = df['education'] * 10  # 根据y值生成大小不同的形状
# plt.scatter(df['categories'], df['education'], marker='o', c=colors, s=area)
# plt.show()

