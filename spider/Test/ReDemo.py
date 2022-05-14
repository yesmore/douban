# -*- coding = utf-8 -*-
# @Time:2021/3/30 13:32
# @Author:anonymity
# @File:ReDemo.py
# @Software:PyCharm

import re

pat = re.compile("AA")

m = pat.search("NBAAcdAA")
d = pat.findall("NBAAcdAA")

print(d)