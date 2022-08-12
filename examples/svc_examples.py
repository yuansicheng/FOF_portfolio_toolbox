#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-12 

import os, sys, argparse, logging

print_old = print
f = open(os.path.join(os.path.dirname(__file__), 'svc_examples_output.txt'), 'w')
def print(s):
    print_old(s)
    f.write(str(s))
    f.write('\n')
    
# 首先将framework的目录加进sys.path中，方便使用相对路径导入
framework_path = os.path.join(os.path.dirname(__file__), '../framework')
if framework_path not in sys.path:
    sys.path.append(framework_path)

# 导入svc
# 所有服务均为singleton， 导入时使用小写服务名
from svc.raw_data_svc.raw_data_svc import raw_data_svc
from svc.date_svc import date_svc

####################################################
####################################################
# raw_data_svc接口示例
print('*' * 50)
print('*' * 50)
print('1. example of raw_data_svc'.upper())
print('*' * 50)
print('*' * 50)

#****************************************************
# 以下不重要

# 设置远程数据库配置文件
# 默认配置文件为raw_data_svc中的db_info.yaml
# 正常使用无需执行该函数
# 配置文件包含ip、用户，密码等
# 输入参数：配置文件路径
print('*' * 50)
print('example of raw_data_svc.setDbConfigFile()')
raw_data_svc.setDbConfigFile(os.path.join(framework_path, 'svc/raw_data_svc/db_info.yaml'))

# 设置表列名配置文件的文件夹地址
# 默认配置文件为raw_data_svc中的table_columns
# 配置文件为每个表有用的列名
# 正常使用无需执行该函数
# 输入参数：路径
print('*' * 50)
print('example of raw_data_svc.setTableColumnPath()')
raw_data_svc.setTableColumnPath(os.path.join(framework_path, 'svc/raw_data_svc/table_columns'))

# 设置本地数据库配置文件
# 默认配置文件为raw_data_svc中的db_info.yaml
# 正常使用无需执行该函数
# 输入参数：配置文件路径
print('*' * 50)
print('example of raw_data_svc.setLocalDbConfigFile()')
raw_data_svc.setLocalDbConfigFile(os.path.join(framework_path, 'svc/raw_data_svc/local_db.yaml'))

#****************************************************
# 以下常用

# 远程查询
# 返回pd.DataFrame
# 输入参数：sql语句
print('*' * 50)
print('example of raw_data_svc.sqlQuery()')
sql = 'SELECT DISTINCT S_INFO_WINDCODE FROM aindexdescription'
data = raw_data_svc.sqlQuery(sql)
print(data)

# 查询完整表
# 优先在本地库中查询，如果本地没有备份，远程查询
# 远程查询完整表时，大表（超过100000行）分年度读取
# 输入参数： tablename-表名，columns-列，一个list，默认查询配置文件中的列
print('*' * 50)
print('example of raw_data_svc.getFullTable()')
data = raw_data_svc.getFullTable('aindexdescription', columns=['S_INFO_WINDCODE', 'OPDATE'])
print(data)

# 获取nav（净值）
# 在净值表（local_db.yaml中nav_tables字段配置）中查找某一个资产
# 净值表sql查询非常慢，只能使用本地表
# 输入参数：tablename-表名，widcode-资产代码
print('*' * 50)
print('example of raw_data_svc.getNav()')
data = raw_data_svc.getNav('chinamutualfundnav', windcode='184688.SZ')
print(data)

print('\n' * 3)


####################################################
####################################################