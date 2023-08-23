import pymysql
import pandas as pd
import os
import time


'''
定义函数get_file
可以获取指定文件夹中所有excel路径名，参数file_dir为该文件夹路径
'''
file_name = []  # 保存文件夹中的每个excel文件路径
dir_name = []  # 保存文件夹中的每个子文件夹路径

def get_file(file_dir):
    for root, dirs, files in os.walk(file_dir):  # root：文件夹所在路径；dirs：文件夹中的所有子文件夹名字list；files：文件夹中所有文件名字list
        for filename in files:
            file_path = os.path.join(root, filename)  # 构建该excel文件的路径
            file_name.append(file_path)  # 把该excel文件的路径添加到file_name列表中
        for dirname in dirs:
            dir_path = os.path.join(root, dirname)
            dir_name.append(dir_path)
    return file_name


'''
定义函数fileTodb
获取excel文件所有sheet数据并上传到数据库，参数path为每个excel文件的路径，需要遍历读取file_name列表的值
'''

def fileTodb(path):
    upload_data = pd.ExcelFile(path)
    for sheetname in upload_data.sheet_names:
        # df = pd.DataFrame(pd.read_excel(open(path, 'rb'), sheet_name = sheetname))  # 将sheet数据转换为dataframe
        df = pd.DataFrame(pd.read_excel(path, sheet_name=sheetname))  # 将sheet数据转换为dataframe

        # ndf = df.where(df.notnull(), 'None') # df.where()筛选 # 快速将缺失值填充为None，不适用于有多种数据类型的df
        # 循环判断不同数据类型的缺失值并填充相应的值
        for col in df.columns:
            if df[col].dtype == "datetime64[ns]":
                df[col].fillna(pd.to_datetime('1900-01-01'), inplace=True)
                df[col] = df[col].dt.date  # 时间格式化，只提取年月日部分
            elif df[col].dtype == "int64":
                df[col].fillna(0, inplace=True)
            elif df[col].dtype == "float64":
                df[col].fillna(0.0, inplace=True)
            else:
                df[col].fillna("None", inplace=True)

        field_name = df.columns.tolist()  # 读取字段名，同时将列表格式转化为字符串格式
        field_num = df.columns.size  # 计算字段个数

        # 计算行数
        # row_num = df.shape[0]
        # # 计算列数
        # col_num = df.shape[1]

        # 设置zhanweifu、colname为空字符串，用来拼接sql语句
        zhanweifu = ""
        colname = ""
        for i in range(0, field_num - 1):
            colname += "`" + str(field_name[i]) + "`,"
            zhanweifu += "%s,"
        colname += "`" + str(field_name[i + 1]) + "`"
        zhanweifu += "%s"
        sheetname = "`" + sheetname + "`"

        # 准备查插改语句
        select = "select * from " + sheetname + ";"
        ins_sql = "insert into " + sheetname + "(" + colname + ")" + " values" + "(" + zhanweifu + ");"
        upd_sql = "update " + sheetname + " set " + colname + "=%s" + " where "

        '''
        【python连接数据库的基本步骤】
        1.导入数据库连接器模块 import pymysql.connect
        2.使用连接器建立连接connect
        3.使用cursor方法创建游标对象
        4.创建mysql查询语句
        5.使用executemany方法执行多条sql语句
        6.提交使用commit方法所做的更改
        7.关闭连接
        '''
        # 创建连接器
        db = pymysql.connect(host="192.168.10.124", user="root", password="ruolin2023", db="ruolindb", port=3306,
                             charset="utf8")

        '''
        try：允许你测试代码块以查找错误
        except：捕捉错误，允许你处理错误
        else：如果没有引发错误，允许执行代码块
        finally：允许你执行代码，无论try和except块的结果如何
        '''
        try:
            with db.cursor() as cursor:
                cursor.execute(select)
                result = cursor.fetchall()
                # result本身是tuple类型，可以用len、（）、not一些方法来判断是否为空元组
                # if len(result) == 0 或 if result == ()
                if not result:
                    # 如果数据是空的，则将data全部插入
                    # 将dataframe的每一行数据转换为tuple，然后整个数据块转换为list，execute函数导入mysql使用
                    data = df.apply(lambda x: tuple(x), axis=1).values.tolist()
                    cursor.executemany(ins_sql, data)
                else:
                    # 将db和df的key转换为set
                    db_set = {row[0] for row in result}
                    df_set = set(df.iloc[:, 0])
                    # 计算交集和差集部分，即区分将要更改或插入的数据
                    upd_set = df_set & db_set
                    ins_set = df_set - db_set  # 以df为主表，即如果df_set有不在db_set的元素就是要插入数据的key值
                    # print("db_set\n", db_set, len(db_set))
                    # print("df_set\n", df_set, len(df_set))
                    # print("ins_set\n", ins_set, len(ins_set))

                    # if upd_set == {}:
                    #     break
                    # else:
                    #     upd_df = df[df[field_name[0]].isin(upd_set)]  # 根据upd_set筛选df数据
                    #     upd_data = upd_df.apply(lambda x: tuple(x), axis=1).values.tolist()
                    #     # cursor.executemany(upd_sql, upd_data)

                    if ins_set == {}:
                        break
                    else:
                        ins_df = df[df[field_name[0]].isin(ins_set)]  # 根据ins_set元素筛选df数据
                        ins_data = ins_df.apply(lambda x: tuple(x), axis=1).values.tolist()
                        cursor.executemany(ins_sql, ins_data)

                db.commit()

        except Exception as e:
            print(f"数据库{sheetname}表操作异常：\n", e)  # 捕捉任何错误并输出
            db.rollback()  # 事务回滚，有commit一定要有rollback，回滚到上次提交的地方
        else:
            print("数据库%s表更新成功！" % sheetname)
        finally:
            cursor.close()  # 关闭游标
            db.close()  # 关闭连接


# 执行主函数，利用windows的定时任务工具实现自动化
if __name__ == "__main__":
    get_file(r'D:\公司共享文件夹\services2023\自动上传(勿删)')
    for path in file_name:
        fileTodb(path)
    time.sleep(3)

# 执行主函数，调用以上两个函数，利用时间函数实现自动化
# if __name__ == '__main__':
#     # 调用get_file()函数
#     get_file(r'C:\Users\Wendy\Desktop\pd')
#     now_time = dt.now()  # 获取当前系统日期和时间
#     now_date = now_time.day  # 获取当前系统日期的日
#     # 当打开程序文件时，while语句会一直循环执行
#     while True:
#         if now_time.minute + now_time.hour * 60 > 5 + 8 * 60 and now_date <= dt.now().day:
#             # for循环将所有excel的所有sheet批量上传
#             for path in file_name:
#                 # 调用fileTodb()函数
#                 fileTodb(path)
#             now_date = now_date + 1
#         # 每隔60s打印一次
#         print(now_date)
#         time.sleep(60)
