# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
from yoctools import *


class Format(Command):
    common = True
    helpSummary = "Format component package.yaml file"
    helpUsage = """
%prog [<component>...]
"""
    helpDescription = """
Format component package.yaml file
"""

    def Execute(self, opt, args):
        yoc = YoC()
        name_list = yoc.get_name_list(yoc.components)
        count = len(args)
        for name in args:
            if name not in name_list:
                put_string("There is no component:%s found." % name, level='warning')
        for component in yoc.components:
            if count == 0 or component.name in args:
                put_string("Formating package: %s." % component.name)
                component.load_package()
                component.pack.save(os.path.join(component.path, 'package.yaml'))
