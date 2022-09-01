#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author	:	yuansc
# @Contact	:	yuansicheng@ihep.ac.cn
# @Date		:	2022-08-29 

import os, sys, argparse, logging

svc_path = os.path.join(os.path.dirname(__file__), '..')
if svc_path not in sys.path:
    sys.path.append(svc_path)

from singleton import Singleton

import yaml

class YamlSvc(Singleton):
    def __init__(self) -> None:
        if not self._isFirstInit():
            return
        print('init YamlSvc')

    def loadYaml(self, yaml_file):
        assert os.path.isfile(yaml_file) and yaml_file.endswith('.yaml')
        # if using py3.8, Loader should be passed
        with open(yaml_file) as f:
            try:            
                return yaml.load(f, Loader=yaml.FullLoader)
            except:
                return yaml.load(f)