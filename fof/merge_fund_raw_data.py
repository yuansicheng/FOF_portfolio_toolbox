#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-10-15

import os, sys, logging

import pandas as pd

from dateutil.parser import parse
from datetime import datetime, timedelta


framework_path = os.path.join(os.path.dirname(__file__), '../framework')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
from alg.alg_base import AlgBase

raw_data_svc = getSvc('LxwWinddbRawDataSvc')
date_svc = getSvc('DateSvc')

date_svc.setTradeDays(raw_data_svc.getTradeDays())


class MergeFundRawDataAlg():
    def __init__(self, ) -> None:
        self._loadRawData()
        self._formatDate()

    def _loadRawData(self):
        logging.info('loading raw data')
        for table, columns in {
            'chinamutualfunddescription': ['f_info_windcode', 'f_info_issuedate',      'f_info_isinitial', 'f_info_delistdate', 'is_indexfund'], 
            'chinamutualfundassetportfolio': ['s_info_windcode','f_ann_date', 'f_prt_stocktotot', 'f_prt_bondtotot'], 
            'chinamutualfundnav': ['f_info_windcode', 'price_date',  'netasset_total'], 
            'chinamutualfundsector': ['f_info_windcode', 's_info_sector'], 
        }.items():
            logging.debug('loading {}'.format(table))
            columns = [c.upper() for c in columns]
            setattr(self, table, raw_data_svc.getFullTable(table, columns))
            getattr(self, table).columns = [c.lower() for c in getattr(self, table).columns]


    def _formatDate(self):
        self.chinamutualfunddescription['f_info_issuedate'] = pd.to_datetime(self.chinamutualfunddescription.loc[:, 'f_info_issuedate'])
        self.chinamutualfunddescription['f_info_delistdate'] = pd.to_datetime(self.chinamutualfunddescription.loc[:, 'f_info_delistdate'])
        self.chinamutualfundassetportfolio['f_ann_date'] = pd.to_datetime(self.chinamutualfundassetportfolio.loc[:, 'f_ann_date'])
        self.chinamutualfundnav = self.chinamutualfundnav.copy()
        self.chinamutualfundnav['price_date'] = pd.to_datetime(self.chinamutualfundnav.loc[:, 'price_date'])

    def _mergeData(self, id_date, qtr_n=4):
        fund_info = self.chinamutualfunddescription[['f_info_windcode', 'f_info_issuedate', 'f_info_isinitial', 'f_info_delistdate', 'is_indexfund']]   # 基金代码、基金发行日、是否是初始基金、退市日期、是否指数基金
        fund_sector = self.chinamutualfundsector[['f_info_windcode', 's_info_sector']]  # 基金代码、基金类型编码
        
        ### 基金净资产规模    # 数据为id_date当天或最近交易日
        # latest_tradeday = [d for d in date_svc.getAllTradeDays() if d <= id_date][-1]
        latest_tradeday = datetime(id_date.year, ((id_date.month-1)//3)*3+1, 1) - timedelta(days=1)
        
        fund_totalNV = self.chinamutualfundnav.loc[self.chinamutualfundnav['price_date']==latest_tradeday]
        fund_totalNV = fund_totalNV[['f_info_windcode', 'netasset_total']]
        
        
        ### 基金持仓-资产配置数据-默认计算id_date前4个季度股票、债券资产平均持仓比例
        # 取最近4个季度股票、债券持仓比例
        fund_allocation = self.chinamutualfundassetportfolio[['s_info_windcode','f_ann_date', 'f_prt_stocktotot', 'f_prt_bondtotot']]
        fund_allocation.fillna(0, inplace=True)
        fund_allocation = fund_allocation.loc[fund_allocation['f_ann_date'] <= id_date]
        fund_allocation.sort_values(by=['s_info_windcode', 'f_ann_date'], ascending=False, inplace=True)
        fund_allocation = fund_allocation.reset_index(drop=True).groupby(by='s_info_windcode').head(qtr_n)
        
        # 计算最近4个季度平均股票、债券持仓比例
        fund_allocation = fund_allocation.groupby('s_info_windcode').mean(numeric_only=True)
        fund_allocation.reset_index(inplace=True)
        fund_allocation.rename(columns={'s_info_windcode':'f_info_windcode'}, inplace=True)    # 修改code列名 后续merge
        
        ### 合并基本信息数据
        fund_list = pd.merge(fund_info, fund_sector, how='left', on=['f_info_windcode'])    # merge基金
        
        fund_list = pd.merge(fund_list, fund_totalNV, how='left', on=['f_info_windcode'])
        fund_list = pd.merge(fund_list, fund_allocation, how='left', on=['f_info_windcode'])
        fund_list['fund_age'] = (id_date -  fund_list['f_info_issuedate']).dt.days/30   # 计算基金年龄(单位：月)
        fund_list['fund_del'] = (id_date -  fund_list['f_info_delistdate']).dt.days/30   # 计算基金停牌时间(单位：月)
        
        # 填充nan
        fund_list['fund_age'].fillna(0, inplace=True)
        fund_list['fund_del'].fillna(-1, inplace=True)
        fund_list['netasset_total'].fillna(0, inplace=True)
        
        ###选取初始基金    #默认 后续可修改
        fund_list = fund_list.loc[(fund_list['f_info_isinitial'] == 1)]
        
        fund_list = fund_list[['f_info_windcode', 's_info_sector', 'fund_age', 'netasset_total', 'f_prt_stocktotot', 'f_prt_bondtotot', 'fund_del', 'is_indexfund']]

        fund_list.drop_duplicates(keep='last')
    
        return fund_list

    def run(self, id_date, qtr_n=4):
        return self._mergeData(id_date, qtr_n=qtr_n)

# # test
# from datetime import datetime
# mfrd = MergeFundRawDataAlg('mfrd')
# print(mfrd.run(datetime(2010,12,5)))

