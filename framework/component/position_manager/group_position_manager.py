#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author    :   yuansc
# @Contact   :   yuansicheng@ihep.ac.cn
# @Date      :   2022-09-21

import os, sys, logging

this_path = os.path.dirname(__file__)
if this_path not in sys.path:
    sys.path.append(this_path)

from position_manager_base import PositionManagerBase

class GroupPositionManager(PositionManagerBase):
    def __init__(self) -> None:
        super().__init__()

        # 单位净值
        self.addPositionData('nav', 1)
        # 份额
        self.addPositionData('shares', 0)
        
    def updateAfterClose(self):
        pass

    def updateAfterOrders(self):
        pass