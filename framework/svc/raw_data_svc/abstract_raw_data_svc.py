#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-12 

import os, sys, argparse, logging

class AbstractRawDataSvc:
    def __init__(self) -> None:
        pass

    def getFullTable(self, table_name, columns=None):
        raise NotImplementedError()


# test
# ardc = AbstractRawDataSvc()
# ardc.getFullTable('')