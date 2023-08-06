#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# ProjectName: HmdUIAutomator
# Author: gentliu
# CreateTime: 2022/1/4 11:19
# File Name: test
# Description:
# --------------------------------------------------------------
import uiautomator2 as u2

if __name__ == '__main__':
    serial = "AQUICKR001LC1800202"
    d = u2.connect(serial)
    hierarchy = d.dump_hierarchy()
    print(hierarchy)

