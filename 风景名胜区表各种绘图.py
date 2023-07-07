import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# 读取只需的数据
wb = pd.read_excel(r'D:\育英-数据处理集训\01-test\风景名胜区.xlsx', sheet_name='风景名胜区')
nwb = wb.query('省份 == "浙江"')[['名称', '总面积(平方公里)', '游客量(万人次)']].reset_index()

del nwb['index']
# print(nwb.isnull())

# 将名称列的值循环读取并赋值给list，另一个方法是list()可以直接将series转化为list
list1=[]
for v in nwb['名称']:
    list1.append(v)

plt.rcParams['font.sans-serif'] = ['SimHei'] # 黑体字体
plt.rcParams['figure.figsize'] = (15, 7)  # 设置绘图窗口尺寸

'''堆积柱形图(在相同的x位置绘制不同的y)'''
x = [i for i in range(len(list1))]
plt.bar(x,nwb['总面积(平方公里)'],width=0.3,color='green',label='总面积')
plt.bar(x,nwb['游客量(万人次)'],width=0.3,color='darkred',label='游客量')
# nwb.plot(kind='bar', color=['green', 'darkred'], width=0.3)
plt.title('浙江省景点面积及游客数量',loc='center',fontsize=20,fontweight='bold')
plt.ylabel('单位：平方千米/ 万人次')
for a, b in zip(x, nwb['总面积(平方公里)']):
    plt.text(a, b, b, ha='center', va='bottom')
for a, b in zip(x, nwb['游客量(万人次)']):
    plt.text(a, b, b, ha='center', va='bottom')
plt.xticks(x,list1,rotation=45) # x1此处可以使用py的内置函数range()
plt.legend(loc=1)
plt.show()

'''折线图'''
plt.plot(nwb['名称'],nwb['总面积(平方公里)'],color='k',linestyle='dashdot',linewidth=1,marker='o',markersize=3,label='总面积(平方公里)')
plt.plot(nwb['名称'],nwb['游客量(万人次)'],color='b',linestyle='dashdot',linewidth=1,marker='*',markersize=3,label='游客量(万人次)')
plt.title('浙江省景点面积及游客数量',loc='center',fontsize=18,fontweight='bold')
x = [i for i in range(len(list1))]
for a,b in zip(x,nwb['总面积(平方公里)']):
    plt.text(a,b,b,ha='center',va='bottom',fontsize=8)
for a,b in zip(x,nwb['游客量(万人次)']):
    plt.text(a,b,b,ha='center',va='bottom',fontsize=8)
plt.xticks(rotation=45)
plt.grid()  # 设置网络线，默认值为True即显示
plt.legend()
plt.show()

'''簇状柱形图(在不同的x位置绘制相同的y，需要调整柱子的显示位置)'''
x1 = [i for i in range(len(list1))] # 用来定位x轴位置
x2 = [i+0.3 for i in range(len(list1))] # 用来定位x轴位置，相对于x1向右偏移了0.3(偏移多少取决于柱形宽度)
plt.bar(x1,nwb['总面积(平方公里)'],width=0.3,color='green',label='总面积')
plt.bar(x2,nwb['游客量(万人次)'],width=0.3,color='darkred',label='游客量')
# nwb.plot(kind='bar', color=['green', 'darkred'], width=0.3)
plt.title('浙江省景点面积及游客数量',loc='center',fontsize=20,fontweight='bold')
plt.ylabel('单位：平方千米/ 万人次')
for a, b in zip(x1, nwb['总面积(平方公里)']):
    plt.text(a, b, b, ha='center', va='bottom')
for a, b in zip(x2, nwb['游客量(万人次)']):
    plt.text(a, b, b, ha='center', va='bottom')
plt.xticks(x1,list1,rotation=45) # x1此处可以使用py的内置函数range()
plt.legend(loc=1)
plt.show()

