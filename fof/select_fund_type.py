#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-10-15

import os, sys, logging

import pandas as pd

from dateutil.parser import parse

this_path = os.path.dirname(__file__)

framework_path = os.path.join(os.path.dirname(__file__), '../framework')
if framework_path not in sys.path:
    sys.path.append(framework_path)

from import_func import getSvc
from alg.alg_base import AlgBase

yaml_svc = getSvc('YamlSvc')

class SelectFundTypeAlg(AlgBase):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._initFundType()

    def _initFundType(self):
        fund_type_data = yaml_svc.loadYaml(os.path.join(this_path, 'fund_type.yaml'), encoding='utf-8')
        self._fund_type_code = fund_type_data['fund_type_code']
        self._fund_type_dict = fund_type_data['fund_type_dict']

    def _getTargetTypeCode(self, type_=None):
        assert type_ in self._fund_type_dict
        return [self._fund_type_code[x] for x in self._fund_type_dict[type_] if x in self._fund_type_code]

    def run(self, fund_info, type_=None):
        return fund_info.loc[fund_info['s_info_sector'].isin(self._getTargetTypeCode(type_=type_))] 

# # test
# sfta = SelectFundTypeAlg('test')
# print(sfta._getTargetTypeCode(type_='stock'))