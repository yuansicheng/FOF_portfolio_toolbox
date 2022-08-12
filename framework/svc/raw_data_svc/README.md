# raw_data_svc

## 一、获取数据库中所有表的列名
python save_table_columns.py  

## 二、选择需要的列名
上一步生成的yaml文件中，注释掉不需要的列。  
使用raw_data_svc读入整表时，只读取配置文件中的列名。

## 三、下载数据到本地
python local_db_storage.py  
将配置文件local_db.yaml中tables设置的表下载到本地，本地数据库位置在local_db_loc字段。

## 四、使用服务
参考示例代码。

