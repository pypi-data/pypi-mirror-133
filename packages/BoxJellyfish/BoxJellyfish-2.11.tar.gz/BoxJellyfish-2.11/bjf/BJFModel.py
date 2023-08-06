#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time:    2021-12-14 23:13
# @Author:  geng
# @Email:   yonglonggeng@163.com
# @WeChat:  superior_god
# @File:    BJFModel.py.py
# @Project: BoxJellyfish
import json
import os
import shutil
from distutils.core import setup

from Cython.Build import cythonize


class ModelAPI():
    def __init__(self):
        self.static_file = None
        self.model_file = None

    def load(self, static_file, model_file, pre, parameters, config=None):
        try:
            shutil.rmtree(pre + "Stages")
        except:
            print("remove over.")
        shutil.copytree(model_file, pre + "Stages/artifacts")
        shutil.copytree(static_file, pre + "Stages/static")

        # try:
        #     shutil.move(static_file, pre + "Stages/static")
        # except:
        #     print("static folder?")

        try:
            setup(ext_modules=cythonize(['UserInterFace.py']), script_args=["build_ext", "-b", pre + "Stages"])
            # shutil.copy("UserInterFace.py", pre + "Stages/")
        except:
            print("UserInterFace ?")
        self.pyfunc_path = os.path.abspath(pre + "Stages")
        if config != None:
            json.dump(config, open(self.pyfunc_path + '/BJFConfig.json', 'w'))

        target_path = pre + "Params"
        target_path = os.path.abspath(target_path)

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        json.dump(parameters, open(target_path + '/parameters.json', 'w'))


class BJFModel(object):
    def __init__(self):
        pass

    def load_model(self):
        self.load_model = None

    def predict(self, data):
        pass
