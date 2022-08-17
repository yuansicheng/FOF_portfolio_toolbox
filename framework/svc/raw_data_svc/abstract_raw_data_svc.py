#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-12 

import os, sys, argparse, logging

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

class AbstractRawDataSvc(Singleton):
    def __init__(self) -> None:
        pass

    def getFullTable(self, table_name, columns=None):
        raise NotImplementedError()


# test
# ardc = AbstractRawDataSvc()
# ardc.getFullTable('')