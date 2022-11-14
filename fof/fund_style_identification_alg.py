#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-10-25 

from email.policy import default
import os, sys, argparse, logging
from symbol import factor

import pandas as pd
import numpy as np
import statsmodels.api as sm

framework_path = os.path.join(os.path.dirname(__file__), '../framework')
if framework_path not in sys.path:
    sys.path.append(framework_path)

this_path = os.path.dirname(__file__)

from import_func import getSvc
from alg.alg_base import AlgBase

constant_svc = getSvc('ConstantSvc')
raw_data_svc = getSvc('LxwWinddbRawDataSvc')

from component.asset.asset import Asset

class FundStyleIdentificationAlg(AlgBase):
    def __init__(self, name, args={}) -> None:
        self.factor_raw_data_path = os.path.join(this_path, 'factors')

        self.look_back = constant_svc.DAY_OF_MONTH*2

        super().__init__(name, args)
        self._setFactorDict()
        self._loadFactorData()

        self._fund_asset = {}

        if self.__class__.__name__ == 'FundStyleIdentificationAlg':
            self._campisi = Campisi('')
            self._stock_fund_identification = StockFundIdentification('')

    def _setFactorDict(self):
        pass

    def _loadFactorData(self):
        pass

    def _loadOneFile(self, file_name, close_col, date_col):
        name = '.'.join(os.path.basename(file_name).split('.')[:-1])
        data = pd.read_csv(file_name)
        data.index = data[date_col]
        if '-' not in str(data.index[0]):
            data.index = pd.to_datetime(data.index, format='%Y%m%d')     
        return name, data[close_col]

    def _loadFactorDataBase(self, path, close_col, date_col):
        self._factor_raw_data = {}       
        for file_name in os.listdir(path):
            name, data = self._loadOneFile(os.path.join(path, file_name), close_col, date_col)
            asset_obj = Asset(name)
            asset_obj.setRawNavData(data)
            self._factor_raw_data[name] = asset_obj

    def _getFactorData(self, id_date):
        factor_data = {k:{} for k in self._factor_dict}
        
        tmp = None
        for group, v in self._factor_dict.items():
            for factor, combination in v.items():
                for asset, weight in combination.items():
                    self._factor_raw_data[asset].setIdDate(id_date, self.look_back)
                    if tmp is None:
                        tmp = weight * self._factor_raw_data[asset].getUsableReturnData()
                    else:
                        tmp += weight * self._factor_raw_data[asset].getUsableReturnData()
                tmp.fillna(method='ffill', inplace=True)
                factor_data[group][factor] = tmp
                tmp = None

            factor_data[group] = pd.DataFrame(factor_data[group])

            # add constant
            factor_data[group] = sm.add_constant(factor_data[group])
        return factor_data

    def _identify(self, id_date, fund_info):
        factor_data = self._getFactorData(id_date)
        exposure = self._getFactorExposure(id_date, fund_info, factor_data)
        return self._getStyle(exposure)

    def _getFactorExposure(self, id_date, fund_info, factor_data):
        exposure = {k:{} for k in factor_data}
        fund_codes = fund_info['f_info_windcode']
        for code in fund_codes.values:
            if code not in self._fund_asset:
                raw_data = raw_data_svc.getNav('chinamutualfundnav', code)
                tmp_asset = Asset(code)
                tmp_asset.setRawNavData(raw_data)
                self._fund_asset[code] = tmp_asset
            self._fund_asset[code].setIdDate(id_date, self.look_back)
            returns = self._fund_asset[code].getUsableReturnData()
            
            if returns.isna().sum():
                continue
            
            for group, df in factor_data.items():       
                exposure[group][code] = self._getFactorExposureOne(returns, df)

        return exposure



    def run(self, id_date, fund_info, type_=None):
        if type_ == 'bond':
            return self._campisi._identify(id_date, fund_info)
        if type_ =='stock':
            return self._stock_fund_identification._identify(id_date, fund_info)


class Campisi(FundStyleIdentificationAlg):
    def __init__(self, name, args={}) -> None:
        super().__init__(name, args)

    def _setFactorDict(self):
        self._factor_dict = {
            'default': {
                'LEVEL': {'CBA00601.CS': 1}, 
                'SLOPE': {'CBA00622.CS': 1, 'CBA00652.CS': -1}, 
                'CREDIT': {'CBA04201.CS': 1, 'CBA02501.CS': -1}, 
                'DEFAULT': {'CBA03801.CS': 1, 'CBA04201.CS': -1}, 
                'CONVERTIBLE': {'000832.CSI': 1}, 
                'EQUITY': {'000985.CSI': 1}, 
            }
        }

    def _loadFactorData(self):
        bond_path = os.path.join(self.factor_raw_data_path, 'bond')
        super()._loadFactorDataBase(bond_path, 'close', 'date')

    def _getFactorExposureOne(self, returns, factor_data):
        # OLS method
        results = sm.OLS(returns, factor_data).fit()
        # print(results.summary())       
        return results.params, results.pvalues

    def _getStyle(self, exposure):
        fund_style = pd.DataFrame(columns=list(exposure.keys()))
        exposure = exposure['default']
        params_dict = {factor: [v[0][factor] for v in exposure.values()] for factor in self._factor_dict['default']}
        # params_p75: largest 25% position
        params_p75 = {factor: np.percentile(v, 75) for factor, v in params_dict.items()}

        
        # the rules
        for code, fund_exposure in exposure.items():
            params, pvalues = fund_exposure[0], fund_exposure[1]
            # the rules
            ##############################
            # conservative
            if pvalues['LEVEL'] <= 0.01 \
                and pvalues['SLOPE'] <= 0.01 \
                and (pvalues[['CREDIT', 'DEFAULT', 'CONVERTIBLE', 'EQUITY']]>0.1).all():
                fund_style.loc[code, 'default'] = 'conservative'
            elif params['LEVEL'] >= params_p75['LEVEL'] \
                or params['SLOPE'] >= params_p75['SLOPE']:
                fund_style.loc[code, 'default'] = 'conservative'
            # active
            elif pvalues['CONVERTIBLE'] <= 0.01 \
                and pvalues['EQUITY'] <= 0.01 \
                and (pvalues[['LEVEL', 'SLOPE', 'CREDIT', 'DEFAULT']]>0.1).all():
                fund_style.loc[code, 'default'] = 'active'
            elif params['CONVERTIBLE'] >=params_p75['CONVERTIBLE'] \
                or params['EQUITY'] >= params_p75['EQUITY']:
                fund_style.loc[code, 'default'] = 'active'               
            # balanced
            elif (pvalues[['LEVEL', 'SLOPE', 'CREDIT', 'DEFAULT']]<=0.05).all() \
                and (pvalues[['CONVERTIBLE', 'EQUITY']]>0.1).all():
                fund_style.loc[code, 'default'] = 'balanced'

        return fund_style
        


class StockFundIdentification(FundStyleIdentificationAlg):
    def __init__(self, name, args={}) -> None:
        super().__init__(name, args)

    def _setFactorDict(self):
        self._factor_dict = {
            'value_growth':{
                'VALUE': {'399371.SZ': 1},
                'GROWTH': {'399370.SZ': 1},
            }, 
            'industry':{
                'FINANCIAL': {'CI005917.WI': 1},
                'CYCLICAL': {'CI005918.WI': 1},
                'CONSUMER': {'CI005919.WI': 1},
                'GROWTH': {'CI005920.WI': 1},
                'STABLE': {'CI005921.WI': 1},
            }, 
            'market_size':{
                'LARGE': {'399314.SZ': 1},
                'MEDIUM': {'399315.SZ': 1},
                'SMALL': {'399316.SZ': 1},
            }
        }

    def _loadFactorData(self):
        stock_path = os.path.join(self.factor_raw_data_path, 'stock')
        super()._loadFactorDataBase(stock_path, 's_dq_close', 'trade_dt')

    def _getFactorExposureOne(self, returns, factor_data):
        rsquare_standerd = {}
        # OLS method
        for factor in factor_data.columns:
            if factor == 'const':
                continue
            result = sm.OLS(returns, factor_data[['const', factor]]).fit()
            rsquare_standerd[factor] = result.rsquared
        # standardization
        rsquare_sum = np.linalg.norm(list(rsquare_standerd.values()))
        rsquare_standerd = {k:v/rsquare_sum for k,v in rsquare_standerd.items()}
        
        return rsquare_standerd

    def _getStyle(self, exposure):
        fund_style = pd.DataFrame(columns=list(exposure.keys()))
        for key, tmp_exposure in exposure.items():
            params_dict = {factor: [v[factor] for v in tmp_exposure.values()] for factor in self._factor_dict[key]}
            # params_p75: largest 25% position
            params_p75 = {factor: np.percentile(v, 75) for factor, v in params_dict.items()}

            for code, fund_exposure in tmp_exposure.items():
                tmp = {k:v for k,v in fund_exposure.items() if v>=params_p75[k]}
                if not tmp:
                    continue
                factor, exposure_max = sorted(tmp.items(), key=lambda x: x[1])[0]
                if exposure_max >= params_p75[factor]:
                    fund_style.loc[code, key] = factor

        return fund_style


# # test
# raw_data_svc = getSvc('LxwWinddbRawDataSvc')
# date_svc = getSvc('DateSvc')
# date_svc.setTradeDays(raw_data_svc.getTradeDays())

# fund_info = pd.read_csv(os.path.join(this_path, 'stock_fund_info_condition.csv'))

# from datetime import datetime
# fsia = FundStyleIdentificationAlg('fsia')
# style = fsia.run(datetime(2015,12,31), fund_info, type_='stock')
# print(style)